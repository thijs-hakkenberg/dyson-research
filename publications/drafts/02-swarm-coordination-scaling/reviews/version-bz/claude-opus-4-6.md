---
paper: "02-swarm-coordination-scaling"
version: "bz"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-28"
recommendation: "Major Revision"
---



# Peer Review: "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms"

**Manuscript Version:** BZ
**Venue:** IEEE Transactions on Aerospace and Electronic Systems

---

## 1. Significance & Novelty

**Rating: 3 (Adequate)**

The paper addresses a genuine gap: the absence of closed-form sizing relationships for coordination architectures at the $10^3$–$10^5$ node scale with byte-level traffic accounting. This is a practically relevant problem as mega-constellations grow and autonomous coordination becomes increasingly necessary. The three-layer feasibility decomposition (byte budget, MAC efficiency, TDMA airtime) is a useful conceptual contribution that could serve as a design checklist for practitioners.

However, the novelty is more incremental than the framing suggests. The core analytical results—overhead scaling as $O(1)$ for hierarchical topologies, coordinator ingress sizing via straightforward throughput calculations, AoI under geometric inter-report intervals, and GE Markov chain recovery—are individually well-known results applied to a specific parameterization. The paper's primary contribution is the *assembly* of these known techniques into a coherent sizing framework, which is valuable but should be presented more modestly. The claim "no prior work provides closed-form parametric sizing relationships" (Section I-A) is strong; while the specific combination may be novel, LEACH analysis, network calculus bounds, and AoI theory each address overlapping subproblems. The paper would benefit from more precisely delineating what is new versus what is a known result applied to a new domain.

The 1 kbps RF-backup regime, which drives most of the interesting constraints, represents a narrow operational scenario ($<$1% of lifetime by the authors' own admission). The paper acknowledges that at $\geq$10 kbps all constraints become non-binding (Table I), which somewhat undermines the practical urgency of the detailed analysis. The operational motivation—safe-mode survivability during ISL outages—is legitimate but should be foregrounded more clearly as the design-driving scenario rather than the general case.

## 2. Methodological Soundness

**Rating: 3 (Adequate)**

The methodology has several strengths: the four-tier verification taxonomy (code, model, packet-level, remaining gap) is well-structured and honestly presented; the separation of $\eta_0$ and $\eta_{\text{cmd}}$ is clean; and the GE parameter sensitivity sweep (Fig. 5b) provides genuinely useful design curves. The open-source commitment strengthens reproducibility.

The fundamental methodological concern is that the DES is cycle-aggregated with fluid-server ingress, meaning it cannot capture the very phenomena that determine feasibility at the 1 kbps design point: MAC contention, slot-level timing interactions, and half-duplex scheduling conflicts. The authors acknowledge this and provide a slot-level TDMA simulator as model verification, which partially addresses the gap. However, the slot-level simulator and the DES implement the *same sizing equations* (as acknowledged in Section IV-J), so their agreement is tautological for overhead metrics. The packet-level CCSDS validation (Section IV-J) is the strongest verification element, as it derives $\gamma$ independently—but it validates only one parameter ($\gamma$), not the full system dynamics.

The Monte Carlo configuration (30 replications) is adequate for mean estimation given the reported SD $< 0.001\%$, but the tail statistics (P99 AoI, P95 GE recovery) deserve more scrutiny. The P99 is computed per-run over $\sim$3.15 × 10⁶ samples, then averaged across 30 runs—this is methodologically sound for the mean of the P99, but the *variability* of the P99 across runs is not reported. For a design equation intended to size safety-critical systems, the distribution of the tail statistic matters. Additionally, the static topology assumption (fixed cluster membership for 1 year) is justified for co-planar formations but the quantitative argument for cross-plane re-association ($<$0.3% overhead, Section V-B) relies on a specific Walker constellation geometry that may not generalize to all deployment scenarios.

The GE channel model coherence assumption (state transitions once per $T_c$) is stated as conservative, and the coherence-time sensitivity analysis (Fig. 4) is a welcome addition. However, the physical mapping (Section IV-C) acknowledges that Earth occultation—the most common ISL outage mechanism—is deterministic and should not use GE at all. This raises the question of what fraction of real outages the GE model actually covers, and whether the stochastic mechanisms (structural shadowing, antenna mispointing) are frequent enough to be design-driving.

## 3. Validity & Logic

**Rating: 3 (Adequate)**

The internal logic is generally sound: the equations are self-consistent, the DES confirms the analytics (by construction), and the packet-level validation genuinely tightens the feasibility boundary. The paper is commendably honest about what is verified versus what remains unvalidated (Table XII).

Several logical issues merit attention:

First, the topology comparison (Section IV-G, Table VIII) is problematic despite the extensive caveats. The paper repeatedly states that the sectorized mesh has different functional scope and that overhead comparisons are "not meaningful," yet presents them side-by-side in multiple tables and figures. If the comparison is not meaningful, it should not occupy significant space; if it is presented, the reader will inevitably draw comparative conclusions. The paper should either commit to a fair comparison (by defining equivalent functional requirements and sizing each architecture to meet them) or remove the sectorized mesh entirely and focus on the hierarchical architecture's absolute performance.

Second, the centralized baseline is modeled as a compute queue only, with no communication overhead. This makes the hierarchical architecture appear to have higher overhead than centralized ($\eta \approx 46\%$ vs. "not applicable"), which is misleading—the centralized architecture's binding constraints (uplink spectrum, propagation latency, ground station availability) are acknowledged but not quantified. The paper should either model centralized communication overhead or remove the centralized column from overhead comparison tables.

Third, the stress-case workload ($p_{\text{cmd}} = 1.0$, 512 B command every cycle to every node) is described as bounding "fleet-wide reconfiguration campaigns," but no evidence is provided that such campaigns actually require per-node-per-cycle commands. Real orbit-raising campaigns (e.g., Starlink) use batch commands with much lower per-node rates. The stress case may be an unrealistically conservative bound that inflates the apparent overhead challenge.

The coordinator failure analysis (Section III-B) is thorough for the optical ISL case but the RF-backup failure scenario ($\sim$160 s recovery) deserves more scrutiny. The compound probability calculation ($6.3 \times 10^{-12}$ s⁻¹) assumes independence between ISL outage and coordinator failure, which may not hold if both are caused by the same event (e.g., a solar particle event affecting multiple subsystems).

## 4. Clarity & Structure

**Rating: 4 (Good)**

The paper is well-organized with a clear roadmap (Section IV introduction) and consistent notation (Table I). The three-layer feasibility framework provides a useful organizing principle. Tables are generally well-constructed, and the cross-model comparison (Table XI) is particularly effective at showing the verification hierarchy.

However, the paper is excessively long for its core contribution. At approximately 12,000 words of body text plus 15+ tables and 10+ figures, it substantially exceeds typical IEEE T-AES length. Much of this length comes from exhaustive caveats, scope notes, and qualifications that, while individually reasonable, collectively obscure the main results. For example, the sectorized mesh model (Section III-B.4) includes a scope note, a connectivity caveat, a functional scope caveat, and a capability matrix—all to present a comparator that the paper says is "not presented as a competing alternative." This material could be condensed to a single paragraph or moved to supplementary material.

The notation is mostly clear but there are some inconsistencies: $p_{\text{link}}$ appears in Table V but is not defined in Table I; $\alpha_{\text{RX}}$ appears in Eq. (7) without prior definition; $\beta$ is introduced in Section III-E.1 but used only briefly. The distinction between $\eta$, $\eta_0$, $\eta_{\text{cmd}}$, $\eta_{\text{total}}$, $\eta_{\text{eff}}$, $\eta_S$, $\eta_E$, and $\eta_{\text{sector}}$ is clear in context but the proliferation of subscripts is taxing.

The abstract is accurate but dense—it reads more like a technical summary than an abstract. The key finding (architecture-specific overhead is small; commands dominate) could be stated more prominently. The introduction's contribution list (items 1–4) effectively previews the results but the operational context paragraph interrupts the flow between contributions and the rest of the introduction.

## 5. Ethical Compliance

**Rating: 4 (Good)**

The paper includes an appropriate AI-assistance disclosure in the Acknowledgment section, identifying specific models (Claude 4.6, Gemini 3 Pro, GPT-5.2) and their role (ideation, not validation). The data availability statement is exemplary, with a specific repository URL, tag, and environment specification. The open-source commitment enables independent verification.

The author block uses a team name with a footnote promising individual names for final publication. While this is acceptable for review, IEEE policy requires named authors with specific contributions. The "Project Dyson Research Team" attribution, combined with the AI disclosure, raises questions about the extent of human intellectual contribution that should be clarified before publication.

One minor concern: the reference to "Claude 4.6" and "GPT-5.2" suggests future model versions that do not exist as of mid-2025, which is unusual and may indicate the manuscript was itself partially AI-generated. The authors should clarify the actual tools used and ensure all claims about methodology are accurate.

## 6. Scope & Referencing

**Rating: 3 (Adequate)**

The paper is appropriate for IEEE T-AES in topic (autonomous spacecraft coordination) but sits at the boundary between a systems engineering sizing study and a communications protocol analysis. The lack of any orbital mechanics simulation, hardware-in-the-loop testing, or real constellation data makes it more of a theoretical framework paper than an aerospace systems paper.

The reference list (55 entries) is comprehensive and generally appropriate. Key works are cited: Lutz et al. for GE channels, Le Boudec for network calculus, Ongaro for Raft, Kaul/Yates for AoI. However, several important related works are missing:

- Radhakrishnan et al. (2016), "Survey of inter-satellite communication for small satellite systems," which directly addresses ISL sizing for small satellite constellations.
- Leyva-Mayorga et al. (2020+), work on non-terrestrial network coordination in 3GPP/NTN context, which addresses similar scaling problems with different assumptions.
- The CCSDS Spacecraft Onboard Interface Services (SOIS) standards, which define coordination protocols for multi-spacecraft systems.
- Recent work on distributed space systems coordination from MIT's STAR Lab or Stanford's GPS Lab.

Several references are non-archival (Amazon Kuiper overview, DARPA program pages, DOD fact sheets) and should be replaced with peer-reviewed sources where possible. The Starlink reference [1] cites an FCC filing supplemented by a personal website—a peer-reviewed analysis of Starlink operations would be more appropriate.

The paper does not cite any prior work on TDMA sizing for satellite systems, which is a well-studied area in the VSAT and mobile satellite literature. The TDMA frame analysis (Section IV-A) would benefit from positioning relative to this existing body of work.

---

## Major Issues

1. **Circular verification architecture.** The DES, slot-level simulator, and analytical equations all implement the same sizing model. Their agreement (Table VII, $<$0.1%) is by construction, not independent validation. Only the packet-level CCSDS validation (Section IV-J) provides genuinely independent confirmation, and it validates only $\gamma$. The paper should clearly distinguish between *internal consistency checks* (DES vs. analytics) and *independent validation* (packet-level, and the missing NS-3 step). The current four-tier taxonomy (Section III-A) conflates these.

2. **Missing MAC-layer dynamics at the design-driving operating point.** The 1 kbps RF-backup regime—where all interesting constraints bind—requires TDMA scheduling, but the DES uses fluid-server ingress. The slot-level simulator addresses superframe timing but not multi-cluster shared-medium effects, which are the binding constraint for fleet-level RF-backup operations (Eq. 5). The paper's central design recommendations (30 kbps coordinator PHY, $\gamma \geq 0.75$) cannot be validated without modeling the shared medium. This is acknowledged (Table XII) but represents a significant gap between the claims and the evidence.

3. **Unfair topology comparison.** Despite extensive caveats, the paper presents overhead numbers for four architectures with fundamentally different functional scopes (Table VIII, Fig. 7). The centralized baseline has no communication overhead modeled; the global-state mesh is an intentional worst case; the sectorized mesh provides different functionality. The only architecture with a complete communication model is the hierarchical one. This framing inflates the apparent advantage of the hierarchical architecture. Either model all architectures at equivalent functional scope or present the hierarchical architecture's absolute performance without comparative claims.

4. **Stress-case workload realism.** The $\eta_S \approx 46\%$ stress case assumes $p_{\text{cmd}} = 1.0$ (512 B command to every node every 10 s cycle). No evidence is provided that any real or planned constellation operation requires this command rate. If the stress case is unrealistic, the paper's most prominent result ($\eta_S \approx 46\%$) is a bound on a scenario that never occurs, and the design implications (TDMA required, coordinator bottleneck) may be artifacts of the assumed workload rather than fundamental architectural properties.

5. **Tail statistic robustness.** The P99 AoI (440 s) and P95 GE recovery (4 cycles) are critical design parameters, but only the mean of the per-run tail statistic is reported. For safety-critical sizing, the *upper confidence bound* on the tail statistic is needed. With 30 replications and $\sim$3.15 × 10⁶ samples per run, the per-run P99 estimates have non-trivial sampling variability. Report the 95% CI on the P99 (partially done for AoI: [438, 444] s) and on the P95 GE recovery.

---

## Minor Issues

1. **Table I notation:** $p_{\text{link}}$ (used in Table V), $\alpha_{\text{RX}}$ (Eq. 7), $\beta$ (Section III-E.1), $f_{\text{RF}}$ (Eq. 5), and $q$ (Eq. 8) are not listed. The notation table should be comprehensive.

2. **Eq. (1):** This is not really an equation—it's a diagram description. Consider removing or replacing with a proper mathematical definition of the hierarchy (e.g., tree depth, fan-out at each level).

3. **Section III-B.2, coordinator service discipline:** "Reports processed at $s_{\text{proc}} = 5$ ms/msg ($\mu_c = 200$ msg/s); $D[k_c]/D/1$ batch latency $\leq 500$ ms." The $D[k_c]/D/1$ notation is non-standard; clarify or cite.

4. **Table III, collision avoidance rate:** $10^{-4}$/node/s seems low for a $10^5$-node constellation. At $N = 10^5$, this gives 10 fleet-wide alerts per second—plausible but should be justified against ESA conjunction statistics [2].

5. **Section IV-A, Eq. (4):** The derived $\gamma = 0.949$ uses only propagation uncertainty and turnaround time. The text then says "conservatively retaining $\gamma = 0.85$" but the packet-level validation derives $\gamma = 0.76$. The progression $0.949 \to 0.85 \to 0.76$ is confusing; consider presenting only the CCSDS-derived value and treating 0.85 as a historical artifact.

6. **Section IV-B, Eq. (9):** The ceiling function produces a step function in AoI vs. $p_{\text{exc}}$, but Fig. 6a shows a smooth curve. Clarify whether the figure shows the continuous approximation or the discrete ceiling.

7. **Table VI, AoI results:** The column header "Max AoI (s)" reports values of 780 s ($p_{\text{exc}} = 0.10$) without confidence intervals. Maximum statistics are highly variable across replications; report the range or CI.

8. **Section III-B.3:** "requires $O(N^2)$ messages for single-cycle convergence via aggressive gossip"—this should be $O(N \log N)$ for standard gossip protocols [ref: Demers et al.]. $O(N^2)$ would be all-to-all broadcast. Clarify the gossip variant assumed.

9. **Acknowledgment section:** "Claude 4.6, Gemini 3 Pro, GPT-5.2" appear to be future/fictional model versions. If these are actual tools used, provide version dates; if placeholder names, use actual model identifiers.

10. **Fig. 1:** Referenced but described only as a PDF include. Ensure the architecture diagram clearly shows the four levels with fan-out ratios and message flow directions.

11. **Section V-B, dynamic topology:** The J2 perturbation analysis assumes a specific Walker constellation. State explicitly that the $<$0.3% overhead estimate is constellation-specific and may not hold for non-Walker geometries (e.g., heterogeneous orbits, elliptical orbits).

12. **Eq. (3):** $B_{\text{sector}}^{\text{capped}} = 256 + \min(k_s - 1, 10) \times 32$ should include units (bytes) in the equation or immediately after.

---

## Overall Recommendation

**Major Revision**

The paper addresses a legitimate gap in the literature and provides a well-structured sizing framework with commendable transparency about limitations and verification status. The three-layer feasibility decomposition, the GE sensitivity design curves, and the packet-level CCSDS validation are genuine contributions. However, the circular verification architecture (DES and analytics implementing the same model), the unfair topology comparison, the unvalidated stress-case workload assumptions, and the missing MAC-layer dynamics at the design-driving operating point represent significant gaps between the claims and the supporting evidence. The paper is also substantially too long for its core contribution and would benefit from significant condensation. A major revision addressing the verification independence, topology comparison fairness, workload realism, and length would make this a solid contribution to IEEE T-AES.

---

## Constructive Suggestions

1. **Sharpen the contribution claim and reduce length by 30–40%.** The core contribution is the three-layer feasibility framework and the design equations (Section V-C). Move the sectorized mesh, global-state mesh, and centralized baseline to a brief appendix or supplementary material. Present the hierarchical architecture's absolute performance (overhead, AoI, GE recovery, coordinator sizing) without comparative framing that requires extensive caveats. This would reduce length by ~4 pages while strengthening the narrative.

2. **Replace the stress-case workload with empirically grounded scenarios.** Contact SpaceX, ESA, or OneWeb operations teams (or cite published operational data) to establish realistic command rates for orbit-raising, conjunction avoidance, and reconfiguration campaigns. If $p_{\text{cmd}} = 0.01$–$0.10$ is more realistic, the stress case becomes $\eta_S \approx 6$–$10\%$, which changes the design implications substantially (TDMA may not be required; coordinator bottleneck vanishes). Alternatively, present the stress case explicitly as a *parametric bound* with a clear statement that realistic workloads are likely much lower.

3. **Implement an NS-3 or OMNeT++ simulation for at least one configuration.** Even a single-cluster ($k_c = 100$) NS-3 simulation with TDMA MAC, half-duplex constraints, and GE channel would provide genuinely independent validation of the coordinator sizing and ARQ infeasibility results. This would close the most critical gap in Table XII and elevate the paper from a theoretical framework to a validated design tool. If full NS-3 is infeasible for this revision, at minimum implement shared-medium contention in the slot-level simulator for the multi-cluster RF-backup scenario.

4. **Report tail statistic uncertainty rigorously.** For all P95/P99 metrics, report the 95% confidence interval across MC replications (partially done for AoI P99). For the GE P95 recovery, report the inter-replication variability. Consider using bootstrap or order-statistic methods appropriate for tail estimation. This is essential for a paper whose stated purpose is to provide *design equations* for safety-critical systems.

5. **Clarify the $\gamma$ progression and commit to a single validated value.** The paper presents three $\gamma$ values (0.949, 0.85, 0.76) from three different models, which is confusing. Present the CCSDS-derived $\gamma = 0.76$ as the validated baseline, show that 30 kbps is feasible at this value, and treat the slot-level $\gamma = 0.949$ as a sub-component that confirms the guard-time contribution. The $\gamma = 0.85$ "conservative assumption" is neither conservative (it's optimistic relative to 0.76) nor validated—retire it.