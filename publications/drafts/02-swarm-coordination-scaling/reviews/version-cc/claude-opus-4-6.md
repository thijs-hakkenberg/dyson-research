---
paper: "02-swarm-coordination-scaling"
version: "cc"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-28"
recommendation: "Unknown"
---



# Peer Review: Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms

## 1. Significance & Novelty
**Rating: 3 (Adequate)**

The paper addresses a genuine gap: closed-form sizing equations for hierarchical coordination at $10^3$–$10^5$ spacecraft scale. The three-layer feasibility decomposition (byte budget, MAC efficiency, TDMA airtime) is a useful conceptual contribution. However, the novelty is tempered by several factors: (a) the core equations are relatively straightforward bandwidth accounting rather than deep analytical results; (b) the "design equations" are largely parameterized ratios of message sizes to channel capacity; (c) the paper's most interesting finding—that command traffic dominates and is topology-invariant under centralized generation—is somewhat obvious once stated. The campaign duty factor $d$ is a welcome addition that substantially improves realism, but it is a simple Bernoulli gating mechanism rather than a methodological advance. The work is useful as a reference sizing tool for practitioners but represents an incremental contribution to the scientific literature.

## 2. Methodological Soundness
**Rating: 3 (Adequate)**

The three-tier verification approach (analytical, DES, slot-level) is well-structured, and the addition of the packet-level $\gamma$ derivation from CCSDS standards is commendable. However, several methodological concerns persist:

- The DES is cycle-aggregated and message-layer only; it necessarily confirms its own equations (acknowledged by the authors). The distributional analysis (Fig. 7) provides some independent value but is limited.
- The slot-level TDMA simulator and packet-level simulator share the same analytical foundations—they are not truly independent verification tools but rather implementations at different granularities of the same model.
- The GE channel model, while grounded in Lutz et al., is applied to ISL self-blockage "by analogy"—this is a significant stretch. ISL channels between co-orbiting spacecraft have fundamentally different propagation characteristics than land-mobile satellite channels.
- The Monte Carlo configuration (30 replications) is adequate for mean estimation but marginal for tail statistics (P99 AoI). The authors report bootstrap CIs, which partially addresses this.

## 3. Validity & Logic
**Rating: 3 (Adequate)**

The internal logic is generally sound, and the paper is careful about stating assumptions. Key observations:

- The campaign duty factor $d$ adequately addresses the earlier concern about workload realism. The decomposition $\eta = \eta_0 + d \cdot \eta_{\text{cmd}}$ is clean and the acknowledgment that the Bernoulli model understates temporal correlation (Section IV-E) is appropriate.
- The $\gamma = 0.76$ unification from CCSDS Proximity-1 is consistently applied throughout and represents a genuine improvement over the earlier assumed 0.85. The decomposition into four sub-efficiencies (Eq. 5, Table IX) is transparent and reproducible.
- The stress-case ($\eta_S \approx 46\%$) is now properly contextualized as a continuous-duty upper bound ($d = 1$), with Table VII showing realistic operating points. This is a significant improvement.
- The three-layer feasibility framework is logically sound but somewhat tautological: Layer 1 is bandwidth accounting, Layer 2 divides by $\gamma$, and Layer 3 checks TDMA slot timing. These are not independent constraints so much as the same constraint expressed at different abstraction levels.
- The claim that the DES provides "distributional analysis" beyond confirming equations is partially supported by Fig. 7 (bimodal ingress CDF), but this is a modest contribution—the bimodality is predictable from the Bernoulli duty-factor model without simulation.

## 4. Clarity & Structure
**Rating: 4 (Good)**

The paper is well-organized with clear notation (Table I), explicit parameter tables, and a logical flow from framework through results to discussion. The roadmap at the beginning of Section IV is helpful. The claim map (Table XIV) is an excellent addition for tracking verification status.

However, the paper is excessively long for its analytical content. Much space is devoted to exhaustive parameter sweeps and cross-checks that confirm what the equations predict. The operational context paragraphs (Introduction) are repeated in multiple forms. Several figures (e.g., Fig. 8, Fig. 10) add little beyond what the tables already convey.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**

The paper provides exemplary transparency: open-source code with tagged release, full parameter tables, explicit AI disclosure, and clear identification of what is modeled vs. unmodeled. The verification taxonomy referencing IEEE 1012 is a good practice. The acknowledgment of the AI-assisted ideation is appropriately handled.

## 6. Scope & Referencing
**Rating: 3 (Adequate)**

The literature coverage is broad but has notable gaps:
- No citation of actual TDMA scheduling literature for satellite networks (e.g., Pratt & Bostian, or the extensive DVB-RCS literature).
- The network calculus reference (Le Boudec) is cited but not actually used—the paper would benefit from either applying it or removing the reference.
- Missing references to actual constellation coordination papers from the operations community (e.g., Flohrer et al. on automated conjunction assessment workflows).
- The GE channel model literature for ISL (as opposed to land-mobile) is not cited because it may not exist—which itself is a concern about the model's applicability.

---

## Major Issues

1. **The DES verification is largely circular, and the paper oversells its independent contribution.**
   - *Issue:* The DES implements the same equations as the analytical model; agreement to <0.1% is expected by construction (acknowledged). The claimed "distributional analysis" (Fig. 7, bimodal CDF) is predictable from the Bernoulli model without simulation. The DES does not model any physics beyond the analytical equations.
   - *Why it matters:* Readers may interpret "DES-validated" as providing independent confirmation, when it is actually implementation consistency checking. The four-tier verification taxonomy (Table XIV) creates an impression of deeper validation than exists.
   - *Remedy:* Reframe the DES contribution more modestly. State explicitly that the DES is a consistency check and bookkeeping tool. Reserve "validation" language for the slot-level simulator and packet-level $\gamma$ derivation. Consider whether the DES results warrant the space they occupy.

2. **The GE channel model is inadequately justified for ISL application.**
   - *Issue:* The Lutz et al. model was developed for land-mobile satellite channels with terrestrial shadowing. Applying it to ISL self-blockage "by analogy" (Section IV-C) is a significant modeling assumption. The three obstruction mechanisms listed (structural shadowing, antenna mispointing, Earth occultation) have different statistical properties than terrestrial shadowing.
   - *Why it matters:* The GE parameterization ($p_{GB}$, $p_{BG}$, $p_B$) drives the recovery analysis, which is a primary contribution. If the parameters are not grounded in ISL-specific data, the recovery curves (Fig. 5) are illustrative but not predictive.
   - *Remedy:* Either (a) cite ISL-specific channel measurement data (if available), (b) present the GE analysis explicitly as a parametric sensitivity study rather than a validated channel model, or (c) derive GE parameters from spacecraft attitude dynamics and antenna patterns for the self-blockage case.

3. **The three-layer feasibility framework, while conceptually clean, conflates dependent constraints.**
   - *Issue:* Layer 1 (byte budget) and Layer 2 (MAC efficiency) are not independent: Layer 2 is simply Layer 1 divided by $\gamma$. Layer 3 (TDMA airtime) adds half-duplex partitioning, which is genuinely new information, but the presentation as "three independent layers" overstates the framework's dimensionality.
   - *Why it matters:* The framework is presented as a primary contribution. If two of three layers are trivially related, the contribution is smaller than claimed.
   - *Remedy:* Reframe as a two-layer framework: (1) message-layer byte budget ($\eta$), and (2) physical-layer schedulability (combining $\gamma$ and TDMA airtime). Alternatively, keep three layers but explicitly acknowledge that Layers 1 and 2 are the same constraint at different abstraction levels, with Layer 3 being the genuinely independent check.

4. **The paper lacks any comparison with or connection to actual constellation operations data.**
   - *Issue:* Despite citing Starlink, Kuiper, and OneWeb, no operational data is used to validate message sizes, reporting rates, or coordination overhead. The 256-byte status report, 512-byte command, and 10-second cycle are assumed without empirical grounding.
   - *Why it matters:* The paper claims to provide "design equations" for practitioners, but practitioners need confidence that the parameterization reflects operational reality.
   - *Remedy:* Add a discussion of how the assumed message sizes compare to CCSDS SPP typical payloads, actual TT&C message sizes from published mission data, or at minimum, provide sensitivity analysis showing how results change if status reports are 128 B or 512 B instead of 256 B.

5. **The topology comparison is structurally unfair and the baselines serve limited analytical purpose.**
   - *Issue:* The centralized baseline models only compute queuing (not communication), the global-state mesh is an intentional worst case, and the sectorized mesh has different functional scope. None is a genuine competing architecture at the same scale.
   - *Why it matters:* Without a meaningful comparator, the hierarchical architecture's overhead cannot be assessed as "good" or "bad"—only as "what it is." The comparison occupies significant space (Tables V, XI, XII; Fig. 9) without providing actionable insight.
   - *Remedy:* Either (a) compare against a realistic alternative (e.g., a two-level hierarchy, or a gossip-based approach with bounded fan-out), or (b) reduce the comparison to a brief paragraph acknowledging the lack of direct comparators and focus the paper on the absolute sizing equations.

## Minor Issues

1. **Table II (bandwidth scaling):** The "Coord. bottleneck?" row answers "Yes (21 kbps)" at 1 kbps but the coordinator operates at 24–30 kbps PHY regardless of $C_{\text{node}}$. Clarify that the bottleneck is relative to the per-node budget, not the PHY rate.

2. **Eq. 8 ($\gamma$ general):** The denominator mixes bits and milliseconds in a way that requires careful unit tracking. Add explicit unit annotations or a worked example.

3. **Section III-B (Coordinator failure transient):** The compound probability calculation ($6.3 \times 10^{-12}$ s$^{-1}$) conflates a rate (ISL outage fraction) with a probability (coordinator failure rate). These have different units and cannot be directly multiplied. Provide a proper compound event calculation.

4. **Table VI (superframe):** The "Unallocated margin = 623 ms" is tight for a system that must also handle clock drift, ranging, and contingency. The paper acknowledges this but does not quantify the probability of margin exhaustion under realistic timing jitter.

5. **Fig. 3 (phase stagger):** The figure is referenced but the experimental setup (random vs. phase-staggered) is not fully described. What is the random-phase model? Uniform over $[0, T_c]$?

6. **Section IV-E (temporal correlation limitation):** The acknowledgment that the Bernoulli model is "exact for mean $\eta$ and conservative (optimistic) for peak buffer occupancy" is important but buried. Elevate this to a more prominent position.

7. **Reference quality:** Several references are "non-archival" (Kuiper, DARPA programs, Replicator). While understandable for program descriptions, the paper should minimize reliance on these for technical claims.

8. **The paper uses "validated" for $\gamma = 0.76$ derived from CCSDS standards.** This is "derived" or "grounded," not "validated" (validation implies comparison with measured data). Consistent terminology per IEEE 1012 would strengthen the paper.

9. **Table VIII (link budget):** Implementation loss of 2 dB is optimistic for a UHF omnidirectional system. Typical values are 3–5 dB including cable losses, impedance mismatch, and depointing. This would reduce the maximum RF-backup rate below 2.5 kbps.

10. **The abstract states "CCSDS Proximity-1 packet-level validation derives $\gamma = 0.76$"—this is a derivation from standards documents, not a validation against measured data.** Rephrase.

11. **Eq. 3 (unicast stagger):** The denominator uses $(1 - \alpha_{\text{RX}})$ but $\alpha_{\text{RX}}$ is not defined until the TDMA frame feasibility paragraph below. Define before use.

---

## Overall Recommendation
**Recommendation: Major Revision**

This paper makes a useful contribution by providing closed-form sizing equations for hierarchical coordination in large spacecraft swarms, with a clean three-layer feasibility decomposition and careful parameter accounting. The standards-grounded $\gamma$ derivation from CCSDS Proximity-1 framing is a genuine improvement that anchors the analysis in physical-layer reality. The campaign duty factor $d$ effectively addresses earlier concerns about workload realism, and the stress-case is now properly contextualized as a continuous-duty upper bound.

However, the paper has significant issues that prevent acceptance in its current form. The DES verification is largely circular and oversold; the GE channel model lacks ISL-specific grounding; the topology comparison is structurally unfair; and the paper is substantially longer than its analytical content warrants. The three-layer framework, while conceptually appealing, conflates dependent constraints. Most critically, the paper provides no connection to operational data, making it difficult for practitioners to assess whether the parameterization is realistic.

The core sizing equations and the $\gamma$ derivation methodology are sound and publishable contributions. A major revision should (1) honestly scope the DES contribution, (2) ground or explicitly qualify the GE parameterization, (3) tighten the presentation by ~30%, and (4) either add operational data comparison or reframe the contribution as a parametric methodology paper rather than a design guide. With these changes, the paper would be suitable for IEEE TAES.

## Constructive Suggestions

1. **Highest impact: Reduce paper length by ~30%.** The DES cross-checks, exhaustive parameter tables, and repeated operational context paragraphs can be condensed without losing content. Move detailed sensitivity sweeps to supplementary material.

2. **Reframe the verification hierarchy honestly.** The DES is a consistency check; the slot-level simulator provides model verification; the $\gamma$ derivation provides standards grounding. Only NS-3 (future work) would provide validation. Use these terms consistently per IEEE 1012.

3. **Ground the GE model or qualify it.** Either derive GE parameters from spacecraft attitude dynamics (structural shadowing duration, frequency, and depth as a function of solar panel geometry) or present the analysis as "if the channel exhibits GE statistics with these parameters, then recovery behaves as follows."

4. **Add a worked design example.** Walk through the sizing equations for a specific mission (e.g., 5,000-node LEO constellation with optical ISL primary and UHF backup). This would demonstrate practitioner utility far more effectively than the current parameter sweeps.

5. **Strengthen the generalized $\gamma$ expression (Eq. 8).** Add a table showing $\gamma$ for 3–4 common space link protocols (Proximity-1, TC-SDLP, CCSDS AOS, custom) to demonstrate the expression's utility. Currently it is presented but not exercised beyond two examples.

6. **Address the topology comparison weakness.** Either add a two-level hierarchy comparator (which would share the same equations with different $k_c$) or reduce the comparison section to a brief discussion acknowledging that the baselines are intentional bounds, not competing architectures.

7. **Quantify sensitivity to message size assumptions.** A simple table showing $\eta_0$ and $\eta_S$ at $S_{\text{eph}} \in \{128, 256, 512\}$ bytes would significantly strengthen the practitioner utility claim.