---
paper: "02-swarm-coordination-scaling"
version: "do"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-03-07"
recommendation: "Unknown"
---

# Peer Review: "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms" (Version DO)

---

## 1. Significance & Novelty
**Rating: 3 (Adequate)**

The paper addresses a genuine gap: closed-form sizing equations for hierarchical coordination in large autonomous spacecraft swarms with byte-level traffic accounting. The two-test feasibility framework (byte budget + TDMA schedulability) is a useful conceptual contribution, and the campaign duty factor formalism is a sensible engineering abstraction. However, the novelty is incremental rather than transformative. The core analytical machinery—TDMA slot efficiency calculations, GE channel modeling, hierarchical message counting—draws heavily on well-established techniques (DVB-RCS2, LEACH, standard queueing theory). The paper's primary contribution is assembling these into a coherent sizing procedure for a specific (and somewhat speculative) application domain. The lack of any flight data, hardware-in-the-loop results, or even high-fidelity orbital simulation limits the practical impact. The target scale ($10^3$–$10^5$ nodes) remains aspirational, making it difficult to assess whether the sizing equations will prove useful in practice.

## 2. Methodological Soundness
**Rating: 3 (Adequate)**

The analytical framework is internally consistent and clearly structured. The decomposition into Test A and Test B is clean, and the rate ladder (Table V) provides a transparent derivation chain. However, several methodological concerns persist:

- The cycle-aggregated DES is acknowledged as a "sanity check" that reproduces analytical means to <0.1%—this is expected by construction and provides minimal independent validation value. The authors are commendably honest about this, but it raises the question of why the DES results occupy space in the paper at all.
- The NS-3 validation is a genuine improvement and the most valuable verification element. However, the NS-3 scenario itself uses significant idealizations (star topology, no Doppler, no orbital dynamics, event-scheduled TDMA). The "independent codebase" claim is valid but the "independent physics" claim is weak.
- The GE channel parameterization is grounded in Lutz et al. for land-mobile satellite channels, but the paper acknowledges these parameters are not validated for ISL scenarios. The sensitivity analysis (Fig. 4) partially mitigates this, but the default parameters remain somewhat arbitrary for the stated application.
- The M/D/c queueing claim for centralized processing (scaling to ~10⁶) is stated without derivation or reference to specific assumptions about processing architecture.

## 3. Validity & Logic
**Rating: 4 (Good)**

The logical structure is generally sound. The two-test framework is well-motivated, and the paper is careful to distinguish between information-layer and physical-layer constraints. Specific strengths:

- The campaign duty factor $d$ is now well-contextualized with Table III mapping mission phases to $(d, p_{\text{cmd}})$ pairs. The claim that $d=1$ represents <1% of operational time is supported by the phase mapping, though the justification could be more rigorous (it relies on the assertion that simultaneous station-keeping + CA occupies $d \leq 0.06$, which is stated without derivation).
- The $\gamma$ unification around 0.73–0.76 via CCSDS Proximity-1 framing is consistently applied throughout. The earlier 0.85 value appears to have been fully replaced. The cross-standard consistency check against DVB-RCS2 (§V) is a valuable addition.
- The stress-case ($\eta_S \sim 46\%$) is now clearly labeled as a continuous-duty upper bound, with Table VI showing the progression from routine to stress.
- The three-layer structure (byte budget, MAC efficiency, TDMA airtime) is logically coherent, and the paper is explicit that $\gamma$ and $\alpha_{\text{RX}}$ are derived quantities within Test B, not independent tests.

One logical concern: the AoI analysis (Eq. 14) assumes independent per-cycle delivery, then immediately notes that GE correlation violates this assumption. The paper handles this by providing the correlated case separately, but the juxtaposition is somewhat confusing.

## 4. Clarity & Structure
**Rating: 4 (Good)**

The paper is well-organized and generally well-written. The notation table (Table I) is helpful, and the rate ladder (Table V) is an effective pedagogical device. Algorithm 1 provides a clear synthesis. Specific observations:

- The abstract is dense but informative; it could benefit from a clearer statement of the primary finding rather than listing multiple quantitative results.
- Section II.A (Related Work) is placed within "System Model" rather than as a standalone section, which is slightly unconventional but acceptable.
- The paper manages complexity well given the number of parameters, tables, and cross-references. The supplementary material is appropriately used for extended derivations.
- Some notation is introduced before being fully defined (e.g., $\eta_0$ appears in the contributions before the overhead decomposition in §II.C).

## 5. Ethical Compliance
**Rating: 4 (Good)**

The AI disclosure is specific and appropriate (Claude 4.6, Gemini 3 Pro, GPT-5.2 for ideation; AI-assisted editing for prose only; no AI-generated results). Data availability is excellent: code, NS-3 scenarios, datasets, and configuration are provided with a specific repository tag. The anonymous authorship ("Project Dyson Research Team") with a note about final publication is acceptable for review but must be resolved. Reproducibility appears strong given the parameter tables and code availability.

## 6. Scope & Referencing
**Rating: 3 (Adequate)**

The reference list covers the major relevant areas (CCSDS standards, DVB-RCS2, swarm robotics, constellation management, DTN, AoI). However:

- The paper would benefit from citing recent work on distributed satellite systems coordination, particularly from the SmallSat/CubeSat community where multi-agent coordination has been demonstrated.
- Network calculus (Le Boudec) is cited but not used; either apply it or remove the citation.
- The self-citation to the "multi-model AI deliberation" tech report (ref [14]) is of questionable relevance and is not peer-reviewed.
- Missing references: recent work on TDMA scheduling for satellite networks (e.g., Marchese et al.), distributed consensus in space systems, and Age of Information in satellite networks.

---

## Major Issues

1. **The DES provides negligible independent validation value.**
   - *Issue:* The cycle-aggregated DES reproduces analytical means to <0.1% because it implements the same equations. The authors acknowledge this ("implementation sanity check") but still present DES results (e.g., AoI confirmation at 441 s vs. 440 s analytical).
   - *Why it matters:* Journal space is consumed by results that confirm arithmetic correctness rather than model validity. This weakens the paper's validation narrative.
   - *Remedy:* Either (a) remove DES results from the main text entirely, relegating them to supplementary material as a code-verification artifact, or (b) modify the DES to include effects absent from the analytical model (e.g., finite queue depths, processing delays, correlated arrivals) and report the *discrepancy* as the interesting result.

2. **NS-3 validation, while valuable, validates MAC timing under idealized conditions—not the system model.**
   - *Issue:* The NS-3 scenario uses a star topology with no Doppler, no orbital dynamics, and event-scheduled TDMA. It validates that the slot-timing arithmetic is correct in an independent codebase, but does not validate the system-level assumptions (static clusters, negligible re-association, spatial reuse feasibility).
   - *Why it matters:* The paper's claims about feasibility at $k_c = 100$, $N = 10^5$ rest on assumptions that the NS-3 validation does not test. The validation addresses the least uncertain part of the model (arithmetic) rather than the most uncertain (physical environment, topology dynamics).
   - *Remedy:* (a) Explicitly scope the NS-3 validation claim: "validates MAC-level timing accounting" rather than implying system-level validation. (b) Add at least one NS-3 scenario with time-varying link quality (e.g., periodic outages simulating orbital geometry) to test robustness of the TDMA schedule. (c) Discuss what *would* be needed to validate the system-level claims.

3. **Spatial reuse ($R \geq 3$) is a critical assumption that remains entirely unvalidated.**
   - *Issue:* Fleet-level feasibility depends on spatial reuse factor $R$, which is stated as "provisional" with $R = 7$ default. The paper acknowledges this but provides no simulation, analysis, or reference to support achievability for the stated antenna configurations and orbital geometries.
   - *Why it matters:* If $R < 3$, fleet-level TDMA becomes infeasible (the paper's own analysis shows $G = 25$ at $R = 1$). This is arguably the most critical assumption for the paper's relevance to the stated scale ($10^5$ nodes), yet it receives the least analytical attention.
   - *Remedy:* (a) Provide a geometric analysis of spatial reuse for representative orbital shells (e.g., Starlink-like 550 km, or a hypothetical Dyson-scale deployment) with specific antenna patterns. (b) At minimum, cite existing work on frequency reuse in LEO constellations and map those results to the paper's assumptions. (c) Consider whether the paper should explicitly restrict its scope to per-cluster sizing and defer fleet-level claims entirely.

4. **The generalized $\gamma$ expression (Eq. 5) needs clearer practitioner guidance.**
   - *Issue:* The paper provides Eq. 5 and Table IV as practitioner tools, but the relationship between $\gamma$ and system-level feasibility is mediated by several other parameters ($\alpha_{\text{RX}}$, $M_r$, egress budget). A practitioner cannot determine feasibility from $\gamma$ alone.
   - *Why it matters:* The stated goal is to provide "design equations" for practitioners. If the $\gamma$ lookup table requires running Algorithm 1 anyway, its standalone utility is limited.
   - *Remedy:* Add a "quick-check" formula that combines $\gamma$ with $k_c$ and $T_c$ to give a single feasibility indicator, e.g., $R_{\text{PHY,min}} \approx k_c \cdot S_{\text{eph}} \cdot 8 / (\gamma \cdot T_c \cdot 0.9)$ (where 0.9 approximates $\alpha_{\text{RX}}$). This would make Table IV immediately actionable.

5. **The $d \leq 0.06$ claim for joint station-keeping + CA needs substantiation.**
   - *Issue:* The paper states that "simultaneous station-keeping + CA events jointly occupy $d \leq 0.06$ in practice" to support the <1% operational time claim for $d = 1$. This is not derived or referenced.
   - *Why it matters:* This is the key claim that makes the stress-case ($\eta_S \sim 46\%$) acceptable as a non-binding constraint. If $d$ is higher in practice (e.g., during initial deployment, orbit-raising, or active debris removal campaigns), the stress case becomes operationally relevant.
   - *Remedy:* Either (a) derive $d$ from published conjunction rates (ESA Space Debris Office reports, cited as [36]) and station-keeping cadences for representative orbits, or (b) weaken the claim to "expected to be small based on current operational experience" with appropriate caveats.

## Minor Issues

1. **Abstract length and density.** The abstract packs too many quantitative results (γ ≈ 0.73–0.76, 27 kbps, 3–8%, 1.8%, 1.5–4.2%, <1%, etc.). Consider focusing on the two or three most important findings and moving details to the body.

2. **Eq. 8 inconsistency.** The feasibility threshold discussion states $P(\text{AoI} > 3T_c) = \epsilon^3$ and then "$P(\text{AoI} > 30\text{ s}) = 10^{-6}$" followed by "$P(\text{AoI} > 30\text{ s}) = 10^{-4}$" two sentences later. The first appears to be for $\epsilon = 0.001$ and the second for $\epsilon = 0.01$, but this is confusing as presented.

3. **Table II footnote.** The footnote states "The 1 kbps per-node budget is a logical traffic allocation within the S-band coordinator's 35 kbps TDMA channel." This important clarification should appear in the main text, not buried in a table footnote.

4. **Network calculus citation.** Le Boudec [29] is cited as providing "deterministic bounds complementary to our mean-value approach" but network calculus is never applied. Either demonstrate the complementarity or remove the claim.

5. **GE parameter justification.** The mapping to Lutz et al. Table 2 (§V) is helpful but should appear earlier (§II.E) where the parameters are introduced, not in the Discussion.

6. **Algorithm 1 line 11.** The ARQ time budget uses $M_r \cdot T_{\text{slot}}$, which assumes worst-case (all retransmissions needed). The text discusses expected retransmissions. Clarify whether Algorithm 1 uses worst-case or expected values.

7. **Figure references.** Fig. 1 (architecture diagram) and Fig. 3 (margin sensitivity) are referenced but their content cannot be verified in this review. Ensure figures are self-contained with complete axis labels and legends.

8. **Eq. 10 notation.** $f_{\text{RF}}$ is introduced in Eq. 10 but not in Table I. Add to notation table.

9. **"Model S" residual.** Eq. 4 (Model S, $\gamma_S = 0.949$) is labeled "not for design" but still occupies space. Consider moving to supplementary material since it serves only as a comparison point.

10. **Typo/formatting.** In Table VI, "Full-load (bcast)" and "Full-load (unicast)" both show $\eta = 46\%$ but different cycle counts. The distinction (broadcast vs. unicast affecting schedulability but not byte budget) should be made explicit in the table caption.

11. **Reference [14].** The self-citation to an unpublished, non-peer-reviewed tech report on "multi-model AI deliberation" is inappropriate for a journal submission. Either publish it or remove the citation and describe the ideation process in the acknowledgment only.

---

## Overall Recommendation
**Recommendation: Major Revision**

This paper makes a legitimate contribution by providing a structured, closed-form sizing framework for hierarchical coordination in large autonomous space swarms. The two-test feasibility decomposition is clean and useful, the campaign duty factor is a well-motivated engineering abstraction, and the CCSDS-grounded $\gamma$ analysis with cross-standard validation against DVB-RCS2 demonstrates careful engineering. The NS-3 packet-level validation is a genuine improvement over purely self-referential DES verification, and the discrepancy decomposition (framing, acquisition jitter, residual) is methodologically sound. The paper is well-written and well-organized for its complexity.

However, several issues require major revision. The most critical is the unvalidated spatial reuse assumption ($R \geq 3$), which is the linchpin of fleet-level feasibility claims at the paper's target scale. The DES verification adds little value and should be either removed or redesigned to test assumptions beyond arithmetic correctness. The NS-3 validation, while valuable, should be more carefully scoped—it validates MAC timing, not system-level feasibility. The $d \leq 0.06$ claim needs substantiation, and the generalized $\gamma$ expression needs clearer practitioner-facing guidance to fulfill the paper's stated design-tool objective.

The paper would also benefit from a clearer delineation between what is validated (per-cluster MAC timing under idealized conditions) and what remains assumed (spatial reuse, static topology, GE parameters for ISL). With these revisions, the paper could make a solid contribution to the preliminary design literature for large-scale autonomous space systems.

---

## Constructive Suggestions
*(Ordered by impact)*

1. **Strengthen spatial reuse analysis.** Add a geometric feasibility analysis for $R$ under representative orbital configurations, or explicitly restrict all claims to per-cluster scope and retitle accordingly.

2. **Enhance NS-3 validation scope.** Add at least one scenario with time-varying link conditions (periodic outages, varying $T_{\text{acq}}$) to test TDMA schedule robustness beyond static conditions.

3. **Provide a single-formula quick-check for practitioners.** Combine $\gamma$, $k_c$, $T_c$, and a conservative $\alpha_{\text{RX}}$ estimate into one inequality that can be evaluated without running Algorithm 1.

4. **Substantiate the $d \leq 0.06$ claim.** Derive from published conjunction rates and station-keeping cadences, or weaken to a clearly stated assumption.

5. **Relocate DES results to supplementary material.** Use the freed space for the spatial reuse analysis or enhanced NS-3 scenarios.

6. **Move GE parameter grounding to §II.E.** The Lutz et al. mapping should appear where parameters are introduced, not in the Discussion.

7. **Add a sensitivity table for $k_c$.** The paper focuses on $k_c = 100$; showing how $R_{\text{PHY,min}}$, $\alpha_{\text{RX}}$, and margin vary across $k_c = 50$–500 would significantly enhance the parametric sizing contribution.

8. **Tighten the abstract.** Focus on the two-test framework, the 35 kbps recommendation, and the NS-3 validation agreement on the feasibility boundary. Move secondary quantitative details to the body.