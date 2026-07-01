---
paper: "02-swarm-coordination-scaling"
version: "at"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-27"
recommendation: "Major Revision"
---



# Peer Review: "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms"

## 1. Significance & Novelty

**Rating: 3 (Adequate)**

The paper addresses a genuine gap at the intersection of mega-constellation operations and swarm coordination: the lack of closed-form design equations for sizing hierarchical coordination architectures at the 10³–10⁵ node scale with byte-level traffic accounting. This is a practically useful contribution. The framing around RF-backup design points is sensible—designers do need to know whether their protocol survives when optical ISLs are unavailable.

However, the novelty is more incremental than the paper suggests. The core analytical results—geometric AoI tails (Eq. 12), Gilbert-Elliott intra-cycle recovery, M/D/1 queueing—are straightforward applications of well-known models. The "design equations" in Section V-C are essentially textbook formulas parameterized for this specific message model. The genuinely novel contribution is the *composition* of these factors and the DES verification that they don't interact under point-to-point ISLs (Section IV-D), but this result is itself acknowledged to be a property of the modeled pipeline rather than a general principle. The paper would benefit from more clearly distinguishing what is new (the specific parameterization, the compositionality verification, the sizing tables) from what is applied textbook material.

The claim in Section I-A that "no prior work has systematically compared coordination architectures for autonomous swarms across 10³–10⁵ nodes using byte-level traffic accounting under a fixed per-node budget" is difficult to verify and somewhat narrow as a novelty claim. The CCSDS community and ESA's space debris office have certainly performed link budget analyses for large constellations, even if not published in the open literature in this exact framing.

## 2. Methodological Soundness

**Rating: 3 (Adequate)**

The cycle-aggregated DES approach is appropriate for the message-layer analysis claimed, and the authors are commendably transparent about what is and is not modeled (Table VII). The Monte Carlo framework (30 replications, bootstrap CIs) is standard and adequate. The analytical cross-checks (DES vs. closed-form matching to within 0.1% for overhead, 1s for AoI) are reassuring.

**However, several methodological concerns arise:**

The simulation is described as "vectorized" with array operations rather than explicit event objects (Section III-A, simulation cycle mechanics paragraph). While this enables fast runtimes (~7s at N=10⁵), it raises questions about whether the simulation actually captures any queueing dynamics at all, or is simply computing the same closed-form equations with random number generation. The near-perfect agreement (SD < 0.001% for overhead) between DES and analytical values across all configurations suggests the simulation may be doing little more than Monte Carlo evaluation of the analytical formulas. If so, calling it "DES-validated" is misleading—it's "Monte Carlo-evaluated." A true DES with event-driven dynamics would show some deviation from the idealized analytical model due to transient effects, boundary conditions, and interaction effects. The authors should clarify what stochastic dynamics the simulation actually captures beyond what the closed-form equations predict.

The static cluster membership assumption (Section III-B.2) is a significant limitation for LEO mega-constellations. The authors acknowledge this but understate its impact. In Walker-delta constellations (Starlink, Kuiper), cross-plane relative motion causes neighbor changes on ~90-minute timescales. For co-orbital planes the assumption is reasonable, but the paper's target regime (10⁵ nodes across multiple shells) necessarily involves cross-plane interactions. The handoff overhead analysis (10–50 MB state transfer) is provided for coordinator rotation but not for cluster re-association, which could be frequent and bursty.

The collision avoidance rate of 10⁻⁴/node/s is stated to represent "screening events, not maneuvers" but the sensitivity analysis (±1.5 pp on η) suggests this parameter has minimal impact regardless. More concerning is that the collision avoidance message flow (128 B alert → coordinator → 512 B evasive command) assumes the coordinator is always reachable within one cycle. Under GE bad-state conditions with P95 recovery of 4 cycles (40s), a time-critical conjunction alert could be delayed by 40+ seconds—potentially unacceptable for close-approach scenarios where TCA uncertainty is on the order of seconds.

## 3. Validity & Logic

**Rating: 3 (Adequate)**

The internal logic of the paper is generally sound, and the authors are admirably careful about qualifying their claims. The distinction between offered and delivered overhead, the explicit MAC-efficiency scaling factor (1/γ), and the conditionality statements on joint independence are all good practice.

**Key validity concerns:**

The "9× envelope" headline (5% to 46%) is dominated by the command workload assumption, not by architectural properties. The authors acknowledge this (Section IV-E: "commands dominate stress-case (>60%)"), but the abstract and introduction frame it as a finding about the architecture. Since commands are topology-invariant (every architecture must deliver commands), the architecture-specific overhead is really just ~5% (summaries + heartbeats), which is a much less dramatic result. The paper would be more honest if it led with "architecture-specific overhead is ~5%; total protocol overhead including commands ranges from 5–46% depending on command rate."

The centralized baseline comparison (Table VIII) is carefully qualified but still potentially misleading. The single-server (c=1) bound diverges at N~10⁴, but the realistic M/D/c model with c=N/k_c doesn't diverge until N~10⁶. The paper correctly identifies the binding centralized constraints as spectrum and ground contact availability, but then the hierarchical architecture's advantage reduces to "fault tolerance during ground outages and spectrum independence"—which, while valid, is a much more modest claim than "hierarchical coordination scales better." The paper should be more forthright that the computational scaling advantage is essentially nonexistent for realistic centralized provisioning.

The joint independence result (Section IV-D, Table IX) is interesting but the explanation is almost tautological: GE losses occur before coordinator ingress, so lost messages never contend for capacity. This is true by construction of the model, not an empirical finding. The "No Loss" and "GE Only" columns in Table IX are *identical*, which confirms that the GE model simply removes messages before they reach the coordinator—the coordinator never "sees" the GE channel at all. This is a valid architectural observation but should not be presented as a simulation finding requiring DES validation.

The AoI-to-position-error coupling (end of Section IV-B) cites ~230 m along-track uncertainty at 441s AoI. This is computed from a constant drift rate (0.5 m/s), but real orbital uncertainty grows nonlinearly due to atmospheric drag uncertainty, solar radiation pressure, and maneuver execution errors. The linear approximation significantly underestimates position uncertainty at 441s for LEO objects.

## 4. Clarity & Structure

**Rating: 4 (Good)**

The paper is well-organized with a clear roadmap (beginning of Section IV) and consistent notation throughout. The practitioner-oriented sizing equations (Section V-C) are a genuine service to the community. Tables are generally well-formatted and informative, particularly the traffic accounting tables (Tables V, VI) and the simulation parameter summary (Table IV).

The writing quality is high, with careful qualification of claims and explicit statements of assumptions. The "Baseline Interpretation Note" (Section I-C) and the operating regime clarification are helpful for readers who might otherwise misinterpret the 1 kbps budget as a nominal operating point.

**Areas for improvement:**

The paper is very long for the depth of its core contributions. Much of Sections III and IV could be condensed. For example, the coordinator link model comparison (Model A vs. Model B vs. TDMA) occupies substantial space but the conclusion is simply "21–50 kbps depending on scheduling assumptions"—this could be a single paragraph with a table. Similarly, the sectorized mesh parameterization (Section III-B.4) receives extensive treatment but serves primarily as an intermediate comparator.

The abstract is dense and tries to convey too many specific numbers. A reader unfamiliar with the domain would struggle to extract the key message. The parenthetical qualifications ("(analytical projection; simulated to 10⁵)," "(DES-validated 95% within 4 inter-cycle retries, mean 1.7 cycles)") make the abstract read like a results summary rather than a motivation-method-finding-implication structure.

Figure references are numerous but the figures themselves are described as PDFs to be included—without seeing the actual figures, it's difficult to assess their effectiveness. The paper references 16 figures, which is high for an IEEE TAES paper and suggests some could be consolidated or moved to supplementary material.

## 5. Ethical Compliance

**Rating: 4 (Good)**

The paper includes an explicit acknowledgment of AI-assisted ideation (Claude 4.6, Gemini 3 Pro, GPT-5.2) in the Acknowledgment section, with appropriate qualification that the AI contributions are "not validated here." The reference to a separate methodology paper [47] is appropriate. The open-source code availability (GitHub with specific tag) supports reproducibility.

The anonymous authorship ("Project Dyson Research Team") with a note that "individual author names and affiliations will be provided for final publication per IEEE policy" is unusual but not unprecedented for pre-publication manuscripts. IEEE policy does require named authors for publication, so this must be resolved.

One concern: the AI model versions cited (Claude 4.6, GPT-5.2) do not correspond to any publicly released models as of the review date. If these are internal/beta versions, this should be clarified; if they are future projections, this raises questions about the manuscript's timeline.

## 6. Scope & Referencing

**Rating: 3 (Adequate)**

The paper is appropriate for IEEE TAES in scope, addressing spacecraft coordination architectures with quantitative analysis. The reference list (50 items) is adequate in breadth, covering constellation operations, swarm robotics, queueing theory, distributed systems, and AoI theory.

**Referencing gaps:**

The paper does not cite several directly relevant works on ISL network design for mega-constellations, including Bhattacherjee et al. (SIGCOMM 2019) on Starlink/Kuiper ISL topology optimization, or the substantial body of work on distributed satellite systems from Schilling et al. and D'Errico (2012). The CCSDS Spacecraft Onboard Interface Services (SOIS) standards, which address intra-spacecraft and proximity communication architectures, are relevant but uncited.

The AoI literature citation is adequate (Kaul, Yates, Kadota) but misses recent work specifically on AoI in satellite networks (e.g., satellite-IoT AoI optimization papers from 2022–2024). The Gilbert-Elliott model is used without citing Gilbert (1960) or Elliott (1963) directly—only the model name is used.

Several references are marked as "non-archival" (Starlink FCC filing, Amazon Kuiper overview, DARPA program pages, DoD fact sheets). While understandable for operational programs, the paper relies on these for motivating claims about current constellation scale and operational approaches. More peer-reviewed sources would strengthen these claims.

---

## Major Issues

1. **Simulation adds minimal value beyond Monte Carlo evaluation of closed-form equations.** The near-perfect agreement (SD < 0.001%, Δ < 0.1%) between DES and analytical values, combined with the vectorized (non-event-driven) implementation, suggests the simulation is essentially computing the same formulas with random sampling. The authors should either (a) demonstrate specific dynamics the DES captures that the closed-form equations do not (beyond the inter-cycle recovery tracking), or (b) reframe the simulation as a "Monte Carlo parametric evaluation tool" rather than a "discrete event simulation" that "validates" the equations. The inter-cycle recovery CDF (Fig. 5) is the one genuinely DES-specific contribution; the rest appears to be analytical verification, not validation.

2. **The joint independence result (Section IV-D) is trivially true by model construction.** The identical drop counts under "No Loss" and "GE Only" conditions (Table IX) confirm that GE losses simply remove messages before they reach the coordinator queue. This is not a finding requiring simulation; it's a direct consequence of the serial pipeline architecture. The paper should present this as a *design principle* (decouple loss recovery from ingress management) rather than an *empirical finding*. The claim that "designers can use the GE recovery and coordinator capacity equations independently" is valid but trivial under the stated architecture.

3. **Static cluster membership invalidates applicability to the stated target regime.** The paper targets 10³–10⁵ node swarms including mega-constellations, but assumes static cluster membership for 1-year simulations. For Walker-delta constellations with multiple orbital planes (the dominant mega-constellation architecture), cross-plane relative motion causes topology changes on ~90-minute timescales. The paper acknowledges this limitation but does not quantify the cluster re-association overhead, which could dominate the protocol overhead budget during active orbital shell transitions. This limitation should be elevated from a discussion point to a scope restriction in the abstract and introduction.

4. **The headline "9× envelope" conflates topology-specific and topology-invariant overhead.** Commands (512 B/node/cycle) account for >60% of stress-case overhead but are required regardless of coordination topology. The architecture-specific overhead (summaries, heartbeats, handoffs) is ~5%, which is the more meaningful architectural comparison. The current framing overstates the architectural significance of the overhead range.

## Minor Issues

1. **Eq. (2):** The M/D/1 mean waiting time formula $W_q = \rho / [2\mu_s(1-\rho)]$ is correct for M/D/1 but should be explicitly noted as the Pollaczek-Khinchine result for deterministic service, not the general M/G/1 formula. The paper mentions P-K validation (Section III-A) but the equation itself should carry the attribution.

2. **Table I:** The "Representative System" column (e.g., "Hyperscale data center" for c=1000) is speculative and potentially misleading. A hyperscale data center could support far more than 1000 parallel message-processing threads.

3. **Section III-B.2, coordinator handoff:** The "seed handoff" mechanism (2 kB, 16s at 1 kbps) for RF-only emergency re-election is described but not modeled in the DES. Its impact on coordination continuity during extended RF-only periods should be quantified or explicitly excluded from claims.

4. **Table IV:** The collision avoidance rate footnote says "Screening events, not maneuver-triggering" but the message flow description (Section III-B.2) describes "evasive commands"—these terms should be reconciled.

5. **Section IV-B:** The AoI P99 formula (Eq. 12) uses ceiling function, but the DES reports 441s vs. analytical 440s. The 1s discrepancy is within the bootstrap CI but the text should note whether this is due to the ceiling function or simulation discretization.

6. **Section V-C, Safe-mode floor:** The formula $\gamma_{\min} = \eta / 1.0$ is dimensionally odd (dividing a percentage by 1.0). This should be $\gamma_{\min} = \eta_{\text{total}}$ where $\eta_{\text{total}}$ is the total channel utilization fraction.

7. **Acknowledgment section:** "Total MC wall-clock time: ~90 min on commodity hardware" is useful but should specify the hardware (CPU, RAM) for reproducibility.

8. **References:** Gilbert (1960) and Elliott (1963) should be cited directly when introducing the GE model. The current text assumes reader familiarity with the model name.

9. **Section III-E:** The statement "Results scale linearly with $C_{\text{node}}$" should be "Protocol overhead fraction $\eta$ is invariant to $C_{\text{node}}$; absolute bandwidth scales linearly."

10. **Table VIII:** The sectorized mesh "Scalability Limit" is listed as ">10⁵ (DES)" but the DES only simulates to 10⁵—this is the maximum tested, not a demonstrated limit.

## Overall Recommendation

**Major Revision**

The paper addresses a legitimate engineering need—sizing equations for hierarchical coordination in large space swarms—and provides a well-organized, carefully qualified analysis. However, the core contributions are more modest than presented: the "design equations" are standard queueing/probability formulas parameterized for a specific message model; the simulation appears to add minimal value beyond Monte Carlo evaluation of these same formulas; and the joint independence result is trivially true by construction. The static topology assumption significantly limits applicability to the mega-constellation regime that motivates the work. A major revision should (1) reframe the simulation's role honestly, (2) address or scope-restrict the static topology limitation, (3) separate topology-specific from topology-invariant overhead in the headline results, and (4) condense the presentation to match the actual depth of contribution. The underlying work is sound and potentially useful to practitioners, but the current framing oversells the novelty and the simulation's role.

## Constructive Suggestions

1. **Reframe the simulation as a parametric evaluation tool, not a validator.** The one genuinely DES-specific contribution—inter-cycle recovery streak tracking (Fig. 5)—should be highlighted as the simulation's unique value. For everything else, be explicit that the DES confirms the closed-form equations rather than discovering new phenomena. This honesty would actually *strengthen* the paper: the message becomes "these simple equations are sufficient for design; no complex simulation is needed."

2. **Add a cluster re-association overhead analysis.** Even an analytical estimate of re-association frequency and state-transfer cost for Walker-delta constellations would substantially strengthen the paper. Use the orbital mechanics to compute how often nodes cross plane boundaries, estimate the state-transfer overhead per event, and show whether it fits within the overhead budget. This would directly address the most significant limitation.

3. **Lead with architecture-specific overhead (~5%) as the primary result.** Restructure the workload envelope discussion to clearly separate the ~5% architecture-induced overhead (summaries, heartbeats, election) from the command-rate-dependent component. This makes the architectural comparison with sectorized mesh more meaningful and avoids the misleading "9× envelope" framing.

4. **Include a packet-level simulation comparison for at least one configuration.** Even a single NS-3 or OMNeT++ run at N=10³ with realistic MAC-layer dynamics would enormously strengthen the paper by grounding the γ assumption and demonstrating whether the message-layer abstraction introduces systematic bias. This is listed as future work (Section V-A) but is arguably necessary for the claims made.

5. **Consolidate figures and reduce paper length by ~20%.** Several figures convey redundant information (e.g., Figs. 7, 9, and 10 all show overhead scaling; Figs. 3 and 6 both address coordinator capacity). Consolidating to ~10 figures and tightening the prose would improve readability and better match the contribution depth to the paper length expected by IEEE TAES.