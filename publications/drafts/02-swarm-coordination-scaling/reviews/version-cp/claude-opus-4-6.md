---
paper: "02-swarm-coordination-scaling"
version: "cp"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-03-03"
recommendation: "Unknown"
---



# Peer Review: Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms

## 1. Significance & Novelty
**Rating: 3 (Adequate)**

The paper addresses a genuine gap: closed-form parametric sizing for hierarchical coordination at the $10^3$–$10^5$ node scale with byte-level traffic accounting. The two-layer feasibility framework (byte budget + TDMA airtime) is a useful conceptual contribution, and the identification of the PHY-rate transition point (24 kbps infeasible → 30 kbps minimum → 35 kbps recommended) is actionable for system designers. However, the novelty is tempered by several factors: (1) the individual analytical components (M/D/1 queueing, GE channel models, AoI analysis, TDMA slot accounting) are well-established; the contribution is their integration rather than methodological advance; (2) the absence of any external validation means the practical significance remains speculative; (3) the paper's primary concrete output—a PHY rate recommendation—is tightly coupled to a specific parameter set ($k_c=100$, $S_{\text{eph}}=256$ B, $T_c=10$ s) whose generality to real missions is undemonstrated.

## 2. Methodological Soundness
**Rating: 3 (Adequate)**

The three-layer feasibility framework (byte budget, MAC efficiency, TDMA airtime) is logically structured, and the paper is commendably careful about distinguishing information-rate from PHY-rate and about not double-counting the $\gamma$ conversion. The campaign duty factor $d$ is a well-motivated addition that substantially improves workload realism—the stress-case contextualization as an episodic upper bound ($<$1% of operational time) is now properly framed. The generalized $\gamma$ expression (Eq. 7) is genuinely useful for practitioners with different link configurations, and the worked examples (Table IX) demonstrate this.

However, several methodological concerns remain:

- The DES verification (Tier 1) confirms its own equations to $<$0.1%, which is expected by construction. The paper acknowledges this honestly, but the distributional tail analysis (buffer sizing under correlated campaigns) is the only genuinely incremental DES contribution, and it rests on assumed campaign statistics with no empirical grounding.
- The GE channel parameterization ($p_{BG}=0.50$, $p_B=0.90$) is acknowledged as a design assumption, but the sensitivity sweep (Fig. 5) is the primary design tool for loss recovery—this is appropriate, though the absence of any ISL measurement data limits confidence.
- The slot-level simulator and the DES share the same underlying model; calling them "cross-model" verification overstates the independence.

## 3. Validity & Logic
**Rating: 4 (Good)**

The internal logic is generally tight and self-consistent. The gamma unification around $\gamma \approx 0.76$ (CCSDS-grounded, replacing the earlier 0.85) appears consistently applied throughout—all feasibility claims, design recommendations, and decision-relevant tables use Model C values. Model S ($\gamma = 0.949$) is clearly labeled as a comparison bound and restricted to Table VI and Fig. 6. The paper is careful to note that Table VI uses Model S slot timing for isolating ARQ×TDMA coupling, not for feasibility claims.

The parameter dependency map (Section IV preamble) correctly separates ingress-side constraints (independent of $d$, $q$) from egress-side constraints, preventing confusion about what drives the 24 kbps infeasibility finding.

The "do not double-count" warning regarding $\gamma$ conversion between layers is a valuable clarification. The distinction between link loss, queue drop, and deadline miss is well-articulated.

One logical concern: the paper claims $\eta$ is "scale-invariant" across $N = 10^3$ to $10^5$, which follows from the hierarchical aggregation structure but assumes perfect load balancing across clusters. Under heterogeneous cluster sizes or non-uniform command distributions, this invariance would break.

## 4. Clarity & Structure
**Rating: 3 (Adequate)**

The paper is extraordinarily dense. While the technical content is thorough, the presentation suffers from information overload. The manuscript reads more like a technical report than a journal article—there are 14 tables, multiple algorithms, and extensive inline derivations that fragment the narrative flow.

**Strengths:** The notation table (Table I) is comprehensive. The rate ladder (Table IV) is an excellent summary artifact. Algorithm 1 is genuinely useful. The slot-timing model distinction (Model C vs. Model S) is clearly stated upfront.

**Weaknesses:**
- The paper is approximately 30% longer than typical IEEE T-AES articles. Significant material could be moved to appendices or supplementary material.
- Section IV is a sprawling 8+ subsection structure that mixes mechanism characterization, verification, sensitivity analysis, and design recommendations without a clear through-line.
- Many footnotes contain substantive technical content that should be in the main text or omitted.
- The repeated caveats ("no external validation exists," "design assumption, not measured") are appropriate but become repetitive—consolidating them would improve readability.
- Some figures are referenced but not shown in the manuscript text (the PDF generation is assumed).

## 5. Ethical Compliance
**Rating: 5 (Excellent)**

The paper is exemplary in its transparency. The validation gap is explicitly acknowledged in multiple locations (abstract, Section III-A, Section V-A, Table XII, conclusion). The AI disclosure is specific about which tools were used and for what purpose. Data availability is comprehensive with tagged repository, specific software versions, and runtime estimates. The V&V tier structure (IEEE 1012) is a mature framing. The paper does not overclaim—the abstract itself states "Results are preliminary design estimates lacking external validation."

## 6. Scope & Referencing
**Rating: 3 (Adequate)**

The reference list (55 items) covers the major relevant areas: CCSDS standards, queueing theory, swarm robotics, constellation management, AoI, and distributed consensus. The DVB-RCS2 reference for partial $\gamma$ anchoring is a good addition. Network calculus (Le Boudec) and the Lutz GE framework are appropriately cited.

**Gaps:**
- No references to actual ISL measurement campaigns (e.g., EDRS, LCRD, or any optical/RF ISL characterization work). Even acknowledging their absence with citations would strengthen the validation gap discussion.
- Limited engagement with the TDMA/MAC scheduling literature beyond CCSDS and DVB-RCS2. The satellite TDMA literature (e.g., Maral & Bousquet, or the extensive DVB-S2/RCS literature) could provide additional context.
- The mean-field game references (Lasry, Huang) seem tangential—they are cited but never used.
- No reference to recent CubeSat swarm demonstrations (e.g., Planet Labs operational practices, or ESA's OPS-SAT) that might provide partial empirical grounding.

## Major Issues

1. **The DES provides negligible independent validation.**
   - *Issue:* The DES reproduces closed-form means to $<$0.1% (acknowledged as "code verification, not model validity"). The distributional tail analysis (buffer sizing) is the sole incremental contribution, but it depends on assumed campaign statistics. The slot-level simulator shares the same model equations. There is no genuinely independent verification pathway.
   - *Why it matters:* The paper's claim structure rests heavily on "DES-validated" and "cross-model" language that implies more independence than exists. A reader might overestimate the confidence level.
   - *Remedy:* (a) Reduce the prominence of DES verification claims—present it as implementation testing, not validation. (b) Consider whether a simplified NS-3 model (even for a single cluster) could provide a genuinely independent MAC-layer check. (c) If NS-3 is out of scope, state this more prominently and reduce the V&V discussion accordingly.

2. **The 1 kbps per-node budget is asserted without sufficient justification.**
   - *Issue:* The entire framework is sized around $C_{\text{node}} = 1$ kbps, described as a "lowest-common-denominator budget." The rationale (coordination during optical outages) is reasonable but the specific value is not derived from any link budget, mission requirement, or operational precedent. Table III shows the UHF backup supports ~2.5 kbps, so 1 kbps is conservative but arbitrary.
   - *Why it matters:* All overhead percentages ($\eta$) scale as $1/C_{\text{node}}$. At 2 kbps, all $\eta$ values halve; at 0.5 kbps, they double. The "46% stress case" and the "35 kbps recommendation" are both artifacts of this choice.
   - *Remedy:* (a) Provide a derivation or operational justification for 1 kbps (e.g., from the S-band link budget divided by $k_c$). (b) Show how the rate ladder shifts for $C_{\text{node}} \in \{0.5, 1, 2, 5\}$ kbps. Table II partially addresses this but only for $\eta$, not for the PHY rate recommendation.

3. **No treatment of multi-cluster RF interference or spatial reuse validation.**
   - *Issue:* Section IV-A.1 introduces fleet-level channel reuse (Eq. 5) but dismisses it as "non-binding" under the assumed parameters. However, at $N = 10^5$ with $k_c = 100$, there are 1,000 clusters potentially sharing RF spectrum. The spatial reuse factor $R = 3$ is assumed without any interference analysis.
   - *Why it matters:* Co-channel interference between adjacent clusters could significantly degrade $\gamma$ or require larger guard bands, invalidating the single-cluster TDMA analysis.
   - *Remedy:* (a) Provide a geometric argument for $R = 3$ (e.g., minimum cluster separation vs. interference range at S-band). (b) Acknowledge that the single-cluster analysis is necessary but not sufficient for fleet-level feasibility. (c) Add this to the validation roadmap with specific NS-3 requirements.

4. **The packet-level validation (Section IV-J) anchors $\gamma$ but does not validate the sizing framework.**
   - *Issue:* The paper correctly states that the CCSDS-grounded $\gamma$ derivation is "parameter anchoring, not framework validation." However, the section title ("Standards-Based Parameter Anchoring") and its prominent placement may lead readers to overestimate its validation contribution. The $\gamma$ derivation is a straightforward calculation from CCSDS specifications—it confirms that the authors correctly read the standard, not that the standard applies to their scenario.
   - *Why it matters:* The gap between "CCSDS Proximity-1 specifies these frame fields" and "ISL TDMA slots in a swarm will achieve $\gamma = 0.76$" is substantial. Real implementations face acquisition failures, Doppler offsets, clock drift accumulation, and antenna pattern variations not captured by the calculation.
   - *Remedy:* (a) Retitle to "CCSDS-Grounded Slot Efficiency Calculation." (b) Add a paragraph discussing the gap between calculated and measured $\gamma$, citing DVB-RCS2 measured efficiencies if available. (c) Quantify the sensitivity: "if measured $\gamma$ is 10% lower than calculated, the minimum PHY rate increases by X kbps."

5. **Static cluster membership assumption is inadequately justified for the claimed scale.**
   - *Issue:* The paper assumes static cluster membership for 1-year simulations, with a brief J2 analysis suggesting $<$0.5% overhead for co-planar clusters. However, at $N = 10^5$, many clusters will necessarily be cross-plane (Walker constellation geometry requires it). The 0.014/orbit re-association rate is fleet-wide, not per-cluster; some clusters will experience much higher rates.
   - *Why it matters:* Frequent re-association triggers state transfers (10–50 MB), Raft elections, and temporary coordination gaps—all of which could dominate the overhead budget during transition periods.
   - *Remedy:* (a) Provide per-cluster re-association statistics (not just fleet-wide mean). (b) Quantify the worst-case cluster's re-association overhead. (c) Discuss whether the hierarchical architecture should be restricted to co-planar clusters, with cross-plane coordination handled differently.

## Minor Issues

1. **Table VI (Joint Interaction) uses Model S but the caption could be more prominent about this.** The footnote explains it, but a reader scanning the table might misinterpret the 24 kbps feasibility result. Consider adding "Model S ONLY" to the table title.

2. **Eq. 6 ($\eta_{\text{consensus}}$):** The variable $N_R$ (Raft rounds) is introduced but not in Table I notation. Add it.

3. **The "thundering herd" analysis (footnote in Section III-B.2)** contains substantive technical content (Slotted ALOHA convergence, BEB parameters) that deserves main-text treatment or should be moved to an appendix.

4. **Table IX (Worked $\gamma$ Examples):** Case 2 (Ka-band) shows $\gamma = 0.422$, which is surprisingly low. The rate-1/2 LDPC dominates; a brief note explaining why rate-1/2 would be chosen at Ka-band (rain fade margin?) would help.

5. **Section IV-B (AoI):** The statement "P99 = 441 s is $<$0.5% of a 24 h TCA window" conflates two different timescales. The AoI P99 is relevant for situational awareness freshness, not for conjunction assessment timelines. Rephrase.

6. **Reference [3] (Amazon Kuiper):** "non-archival; accessed February 2026" suggests a future access date. Verify.

7. **The abstract mentions "CCSDS Proximity-1 framing anchors $\gamma \approx 0.76$"** but the body shows $\gamma_{24} = 0.761$ and $\gamma_{30} = 0.745$. The abstract should note the rate dependence or use the more conservative value.

8. **Algorithm 1, Line 3:** The expression for $\eta_{\text{total}}$ appears to omit the heartbeat and summary components of $\eta_0$. Clarify whether $\eta_0$ is a constant or computed.

9. **Table VII (Superframe):** The sync beacon is listed as 0.3 ms (8 bits at 30 kbps) but placed under "Ingress (RX)" while labeled "TX." Move to egress or create a separate sync category.

10. **The paper uses both "kbps" and "bps" without consistent formatting.** Adopt SI conventions throughout (kbit/s or use the siunitx package consistently).

11. **Fig. 5 caption:** "DES bars (30 MC replications, $N = 10,000$, $k_c = 100$)"—the figure shows both (a) and (b) panels but the caption describes only (a) in detail. Add description for panel (b) markers.

12. **Section V-C (Design Equations Summary):** The $\gamma$-conditional PHY lookup table ($[0.65, 0.70] \Rightarrow 40$ kbps, etc.) is useful but should note it applies specifically to $k_c = 100$, $S = 256$ B, $T_c = 10$ s.

## Overall Recommendation
**Recommendation: Major Revision**

This manuscript tackles a worthwhile problem—parametric sizing for hierarchical coordination in large space swarms—and provides a carefully constructed analytical framework. The two-layer feasibility decomposition (byte budget + TDMA airtime) is sound in concept, and the paper is commendably honest about its limitations, particularly the absence of external validation. The campaign duty factor $d$ effectively addresses workload realism, and the CCSDS-grounded $\gamma$ derivation (replacing the earlier 0.85) is consistently applied throughout. The generalized $\gamma$ expression with worked examples for different link configurations is genuinely useful for practitioners.

However, the paper suffers from three fundamental issues that require major revision. First, the validation structure is weaker than presented: the DES confirms its own equations, the slot-level simulator shares the same model, and the CCSDS $\gamma$ derivation is a calculation rather than a measurement—the paper needs to more honestly characterize the evidence base and reduce the prominence of "validation" language. Second, the 1 kbps per-node budget, which drives all quantitative results, lacks sufficient justification; a sensitivity analysis across budget values is essential. Third, the manuscript is substantially too long and dense for a journal article, with material that belongs in supplementary documentation mixed into the main narrative.

The strongest elements—the rate ladder (Table IV), Algorithm 1, the $\gamma$ sensitivity framework (Eq. 7 + Table IX), and the margin analysis (Table VIII)—should be preserved and made more prominent. The weaker elements—extensive DES verification of known equations, repeated caveats, and tangential material—should be condensed. With these revisions, the paper could make a solid contribution to the spacecraft systems engineering literature as a design reference.

## Constructive Suggestions

1. **Restructure as a shorter, more focused paper** (~8,000 words vs. current ~12,000+). Move the DES distributional analysis, GE mechanism mapping table, and thundering-herd analysis to supplementary material. Focus the main paper on: (a) the two-layer framework, (b) the $\gamma$ derivation and rate ladder, (c) the duty-factor parameterization, and (d) the feasibility algorithm.

2. **Add $C_{\text{node}}$ sensitivity analysis.** Show the rate ladder for $C_{\text{node}} \in \{0.5, 1, 2, 5\}$ kbps. This would demonstrate the framework's generality and help practitioners with different link budgets.

3. **Strengthen the validation narrative** by (a) clearly labeling all internal checks as "implementation verification," (b) adding a single-cluster NS-3 simulation (even simplified) as a genuinely independent check, and (c) providing measured $\gamma$ values from any available TDMA satellite system (DVB-RCS2 terminals, Iridium, etc.) as external anchoring points.

4. **Add a spatial reuse analysis** for multi-cluster RF interference, even if simplified (e.g., minimum separation distance for $R = 3$ at S-band with specified antenna patterns).

5. **Create a one-page "practitioner's guide"** (possibly as an appendix) that walks through Algorithm 1 with a concrete example different from the default parameters, demonstrating the framework's flexibility.

6. **Consolidate the validation gap discussion** into a single, prominent subsection rather than distributing caveats throughout. This would be more impactful and less repetitive.