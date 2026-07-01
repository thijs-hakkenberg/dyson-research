---
paper: "02-swarm-coordination-scaling"
version: "r"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-24"
recommendation: "Major Revision"
---

# Peer Review: "Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study"

## IEEE Transactions on Aerospace and Electronic Systems

---

## 1. Significance & Novelty

**Rating: 3 (Adequate)**

The paper addresses a genuinely important problem: how to coordinate autonomous spacecraft swarms at scales of 10³–10⁵ nodes. The motivation is timely given Starlink's growth trajectory and planned mega-constellations. The paper correctly identifies that the combination of autonomous (non-ground-directed) coordination, byte-level traffic accounting, and 10⁴–10⁵ node scale is underexplored in the literature. The introduction of Age-of-Information as a coordination quality metric for space swarms, the coordinator bandwidth stress-testing, and the sectorized mesh comparator are useful engineering contributions.

However, the central novelty claim is substantially weakened by the paper's own admissions. The $O(1)$ overhead scaling of the hierarchical architecture is, as the authors correctly state (Section IV-D), "a direct mathematical consequence of the hierarchical message structure—not a surprising emergent property." The DES then confirms this analytical result to within 0.05% at all fleet sizes (Table V), which validates the implementation but does not constitute a discovery. The paper is essentially a careful accounting exercise that quantifies the protocol coefficient of a well-understood hierarchical message-passing structure. While quantification has engineering value, the intellectual contribution is modest for a top-tier journal.

The claimed gap in the literature—"no prior work has systematically compared coordination architectures for autonomous spacecraft swarms across the 10³–10⁵ range"—deserves scrutiny. The networking literature on satellite mega-constellations (Handley 2018, Del Portillo et al. 2019, Akyildiz et al. 2003) addresses routing and capacity at comparable scales, albeit with different abstractions. The paper would benefit from a more nuanced positioning relative to this body of work, explaining precisely what the message-passing abstraction layer reveals that existing ISL routing studies do not.

## 2. Methodological Soundness

**Rating: 3 (Adequate)**

The simulation framework is described with commendable transparency. The abstraction scope table (Table III), traffic accounting (Table IV), and parameter summary (Table II) are exemplary in their completeness. The analytical cross-check (Section IV-D, Eq. 10) is a valuable validation step. The authors are refreshingly honest about the near-deterministic nature of their model (SD < 0.001%), which is a strength of the presentation even as it raises questions about the necessity of 30 Monte Carlo replications.

The fundamental methodological concern is **circularity**, which the authors partially acknowledge in Section V-E. The DES operates at the message-passing layer and abstracts away precisely the physical-layer phenomena (MAC contention, link acquisition, correlated outages, half-duplex constraints, antenna scheduling) most likely to introduce scale-dependent nonlinearities. The paper then claims the DES confirms "no queueing-induced nonlinearities" across two orders of magnitude—but the model is constructed in a way that makes such nonlinearities nearly impossible to observe. The coordinator queueing model operates at ρ = 0.05 for k_c = 100, far from any saturation regime. The message model is deterministic (fixed sizes, fixed rates). The only stochastic element is the 2%/year failure process, which perturbs a negligible fraction of nodes per cycle. Under these conditions, the DES is essentially computing the same closed-form expression as Eq. 10, with floating-point noise as the only source of variance.

The Bernoulli link availability model (Section IV-F) is a useful extension but remains a significant simplification. In LEO, link outages are dominated by Earth occlusion, which produces deterministic, correlated, periodic outages—not i.i.d. per-message losses. The authors acknowledge this (Section V-E) but the gap between the model and reality is large enough to question whether the retransmission robustness envelope (the paper's fourth claimed contribution) would hold under realistic link dynamics.

The sectorized mesh comparator (Section III-B.4) is a welcome addition but its parameterization raises questions. The capped-fanout variant (≤10 heartbeat neighbors) produces $O(N)$ scaling by construction—the cap is what forces linearity. The 2.2× overhead ratio relative to hierarchical is therefore a direct consequence of the parameter choice (10 heartbeats × 32 B vs. 1 report × 256 B + overhead), not an emergent property of the topology. The uncapped variant, which would provide a more meaningful comparison, is analyzed only analytically.

## 3. Validity & Logic

**Rating: 3 (Adequate)**

The paper's conclusions are internally consistent and well-supported within the stated abstraction level. The authors deserve credit for the extensive qualification of their results: the baseline interpretation note (Section I-C), the model-form uncertainty band (η_eff ∈ [18%, 27%]), the explicit acknowledgment that the centralized baseline is a worst-case bound, and the detailed limitations section (V-E) all demonstrate intellectual honesty.

However, several logical issues merit attention:

**The "actionable design parameters" claim is overstated.** The coordinator bandwidth thresholds (50 kbps unscheduled, 24 kbps TDMA) are derived from a model that assumes uniform random phase offsets within T_c, fixed message sizes, and no MAC-layer effects beyond a scalar efficiency factor γ. These thresholds are properties of the model parameterization, not of physical ISL hardware. Calling them "directly actionable hardware sizing constraints for ISL radio design" (Section I, contributions) overpromises relative to the abstraction level.

**The AoI analysis, while valuable, has a logical gap.** The paper correctly identifies that P99 AoI > 400 s at p_exc = 0.10 must be "traded against conjunction screening timelines." But the paper does not establish what AoI threshold is operationally meaningful. Without coupling to orbital prediction accuracy and conjunction detection probability, the AoI numbers are descriptive but not prescriptive. The paper acknowledges this (Section IV-E, "Limitations of the AoI metric") but still lists it as the first contribution.

**Table I (cluster size results) shows suspiciously uniform overhead values.** The overhead varies by only ±0.2% across k_c = 50 to 500, which the authors explain by noting that the dominant η components scale with N regardless of k_c. This is correct but raises the question: if overhead is invariant to the primary design parameter, what does the DES add beyond the analytical formula? The latency variation (340–675 ms) is more informative but is driven entirely by regional coordinator queueing, which is itself a function of the parameterization (n_r = 10, μ_r = 500 msg/s).

**The exception-based telemetry validation (Table VI) confirms the law of large numbers**, as the authors note. The DES-measured reduction factors match the Bernoulli expectation to within 1% for N × T/T_c ≫ 1 independent trials. This is expected and does not require simulation to establish.

## 4. Clarity & Structure

**Rating: 4 (Good)**

The paper is well-organized and clearly written, with a logical flow from problem statement through methodology, results, and discussion. The extensive use of tables (13 tables) and figures (10 figures) supports the narrative effectively. The abstraction scope table (Table III) and traffic accounting table (Table IV) are particularly useful for understanding exactly what is and is not modeled.

The abstract is comprehensive but dense—at approximately 250 words, it attempts to convey too many specific numerical results. A more focused abstract highlighting 2–3 key findings would be more effective for the target readership.

The paper is long (approximately 14 pages of dense content) and could benefit from consolidation. Several results are presented multiple times in different forms: overhead scaling appears in Tables I, V, and VII, and in Figures 2, 5, and 6. The analytical cross-check (Section IV-D) could be shortened since the agreement is exact by construction (the DES implements the same traffic model as the analytical formula).

The notation is generally consistent, though the use of η for protocol overhead (excluding baseline telemetry) and η_total for total utilization requires careful tracking. The distinction between "offered load" and "delivered overhead" in Table VIII is important and well-explained.

One structural weakness: the paper front-loads extensive methodology (Sections III-A through III-G, approximately 5 pages) before presenting any results. Given that the methodology is largely a careful parameterization exercise rather than a novel simulation technique, some of this material could be moved to an appendix or supplementary material.

## 5. Ethical Compliance

**Rating: 4 (Good)**

The paper includes an appropriate acknowledgment of AI-assisted ideation (Claude 4.6, Gemini 3 Pro, GPT-5.2) in the Acknowledgment section, with a clear statement that the AI-generated concepts are "not validated in the current study." This is transparent and appropriate. The data availability statement promises open-source code and datasets, which supports reproducibility, though the commit hash is listed as "[PENDING]."

The author attribution is unusual—"Project Dyson Research Team" with a footnote promising individual names for final publication. This is acceptable for review but must be resolved before publication per IEEE policy.

The paper does not discuss dual-use concerns related to military swarm applications, despite citing DARPA OFFSET, Blackjack, and the Replicator initiative. Given that the coordination architectures described are directly applicable to military drone swarms (acknowledged in Section V-A), a brief discussion of dual-use implications would be appropriate for a journal of this stature.

## 6. Scope & Referencing

**Rating: 3 (Adequate)**

The paper is appropriate for IEEE T-AES in its focus on autonomous spacecraft coordination, though it reads more as a communications/networking study than an aerospace systems paper. The connection to actual spacecraft operations is thin—the orbital mechanics are simplified, the failure model is generic, and the coordination tasks (collision avoidance, orbit adjustment) are modeled only as message types with fixed sizes rather than as operational workflows with mission-specific requirements.

The reference list (47 citations) is adequate but has notable gaps. The paper does not cite:
- Recent work on distributed space situational awareness (e.g., Hobson et al., Frueh et al. on distributed conjunction assessment)
- The substantial literature on networked control systems with communication constraints (e.g., Hespanha, Nair & Evans on data-rate limited control)
- Recent mega-constellation simulation studies (e.g., Portillo et al. 2019 is cited but more recent capacity analyses are missing)
- The DTN/BPv7 literature is cited but not engaged with—BPv7 store-and-forward is listed as "abstracted" in Table III but could fundamentally change the coordinator bandwidth analysis

Several references are non-archival (SpaceX website, Amazon website, DARPA program pages, DoD fact sheets). While understandable for operational systems, the paper relies on these for key claims about current constellation scale and operations. At least 6 of 47 references are non-archival web sources, which is high for a journal paper.

The paper cites future model versions (GPT-5.2, Claude 4.6, Gemini 3 Pro) that do not exist as of the review date, suggesting either speculative naming or a future publication date assumption. This should be clarified.

---

## Major Issues

1. **The DES adds minimal value beyond the analytical formula.** The close agreement between η_DES and η_analytic (within 0.05% at all scales, Table V) demonstrates that the DES is computing the same quantity as Eq. 10. The claimed DES contributions—protocol coefficient quantification, queue stability confirmation, and analytical cross-check—are all consequences of the model's near-deterministic structure. The paper needs either (a) a more complex model where the DES reveals behavior not predictable analytically, or (b) a reframing that positions the DES as a validation tool rather than a discovery instrument. The AoI analysis and coordinator bandwidth stress test are the strongest candidates for genuinely simulation-dependent results and should be elevated.

2. **The physical-layer abstraction undermines the scalability claim.** The paper's central engineering claim—that hierarchical coordination maintains ~21% overhead from 10³ to 10⁵ nodes—is valid only within the message-passing abstraction. The authors acknowledge (Section V-E) that MAC contention, correlated link outages, and priority queueing could introduce scale-dependent effects, but these are precisely the phenomena that matter for real system design. Without at least a minimal MAC-layer model (e.g., TDMA slot scheduling within T_c, as the authors themselves identify as priority future work), the scalability claim cannot be extended to physical systems with confidence. This is not a fatal flaw but significantly limits the paper's applicability.

3. **The comparison architecture is incomplete.** The sectorized mesh comparator is a useful addition, but the capped-fanout parameterization (≤10 neighbors) makes the comparison somewhat artificial. The 2.2× overhead ratio is a direct consequence of the parameter choice. A more meaningful comparison would include: (a) the uncapped sectorized mesh implemented in the DES (not just analyzed analytically), (b) a two-level hierarchy (cluster + ground, no regional tier) to isolate the contribution of each hierarchical level, and (c) a hybrid architecture where sectors use hierarchical aggregation internally—which the authors note (Section V-C) "closely resembles the hierarchical architecture studied here."

4. **The coordinator bandwidth analysis conflates offered-load modeling with hardware sizing.** The 50 kbps (unscheduled) and 24 kbps (TDMA) thresholds are derived from a byte-budget queue model with uniform random phase offsets. Real coordinator ingress involves link acquisition delays (1–5 s per new link, per Table III), Doppler compensation, half-duplex turnaround, and antenna beam scheduling—all of which are abstracted away. Presenting these thresholds as "directly actionable hardware sizing constraints" overstates the model's fidelity.

---

## Minor Issues

1. **Abstract, line 3**: "cycle-aggregated discrete event simulation (DES) at the message-passing abstraction layer" — the term "cycle-aggregated DES" is non-standard. Consider defining it more precisely or using established terminology (e.g., "time-stepped simulation with event-driven sub-resolution").

2. **Section III-A**: The claim that "inter-arrival coefficient of variation at the centralized server is 0.98 ± 0.03 for N ≥ 1,000" validates the Poisson assumption is correct but the Palm-Khintchine theorem requires independent sources, which is satisfied here. The citation to Kleinrock [28] is appropriate but a more specific reference to the superposition theorem would strengthen the argument.

3. **Eq. 4 and surrounding text**: The message complexity is stated as O(N) "with fixed hierarchy depth," but the hierarchy depth is always fixed at 4 levels in this study. The qualifier is unnecessary and slightly misleading—it suggests the result might not hold with variable depth.

4. **Table II**: The collision avoidance rate footnote (a) explains the 10⁻⁴/node/s rate well, but the 1,000:1 screening-to-maneuver ratio should be cited. The ESA Space Debris Office report [47] is cited for maneuver rates but not for the screening ratio.

5. **Section IV-B, latency budget**: The statement that "serialization of a 256 B message over a 1 Gbps optical ISL takes ~2 μs, which is negligible" is correct but inconsistent with the earlier statement (Section III-A) that "messages experience... size-dependent serialization delay (significant for large handoff transfers but negligible for status reports)." Clarify that serialization delay is computed at the physical link rate, not the 1 kbps budget rate.

6. **Table V**: All ten fleet sizes show identical η_DES = 20.7%. While this is the expected result, presenting ten identical rows adds no information. Consider condensing to "η_DES = 20.7% ± 0.0% across all N ∈ {10³, ..., 10⁵}" and using the table space for more informative data (e.g., per-tier breakdown at each scale).

7. **Section IV-C (Duty Cycle)**: The handoff success rates (95.0% at 1h to 99.9% at 7d) are presented without derivation. What reliability model produces these specific values? The text mentions "our reliability model" but does not specify it.

8. **Figure 3 caption**: States the 10⁶-node curve is an "analytical extrapolation," which is appropriately flagged. However, this figure appears before the text establishing that DES validation covers only 10³–10⁵, potentially misleading readers who scan figures before text.

9. **Section III-F**: The per-node bandwidth breakdown (Table VI) shows analytical estimates of ~9% overhead for hierarchical, while the DES measures ~21%. The footnote (b) explains this discrepancy but the presentation is confusing—two different overhead definitions appear in the same section.

10. **References**: [1] (SpaceX), [3] (Amazon Kuiper), [16] (DARPA OFFSET), [18] (DoD Replicator), [22] (DARPA Blackjack) are all non-archival web sources. Consider replacing with peer-reviewed alternatives where possible, or at minimum adding access dates consistently.

11. **Eq. 6 (mesh convergence)**: The claim D = O(N^{1/3}) for a random geometric graph in 3D orbital space is stated without proof or citation. Orbital geometries are not random geometric graphs—they are constrained to shells and planes. This approximation should be justified or qualified.

---

## Overall Recommendation

**Major Revision**

The paper addresses an important problem with commendable methodological transparency and intellectual honesty. The AoI analysis, coordinator bandwidth stress-testing, and sectorized mesh comparator are genuine contributions. However, the central result (O(1) overhead scaling) is analytically trivial, and the DES confirms it to a degree that raises questions about the simulation's added value. The physical-layer abstraction limits the applicability of the quantitative results to real system design. A major revision should: (1) reframe the contribution around the engineering design parameters (AoI thresholds, coordinator capacity, retransmission envelopes) rather than the scaling property; (2) add at least a minimal MAC-layer model to test whether the O(1) scaling survives physical-layer effects; (3) strengthen the sectorized mesh comparison with the uncapped variant in the DES; and (4) reduce redundancy in the presentation of overhead scaling results.

---

## Constructive Suggestions

1. **Elevate the AoI and coordinator bandwidth results to primary contributions; demote the O(1) scaling confirmation.** The AoI trade-off curve (Fig. 8) and the coordinator capacity thresholds (Tables IX–X) are the results most useful to practicing engineers. The O(1) scaling is analytically guaranteed and its DES confirmation, while valid, is not surprising. Restructuring the paper around "what design parameters does a hierarchical swarm architect need?" rather than "does hierarchical scaling work?" would significantly strengthen the contribution.

2. **Implement a minimal TDMA scheduling model within the DES.** The authors identify this as priority future work (Section V-E), but it is achievable within a revision cycle. Dividing T_c into k_c slots with guard intervals and simulating slot-level contention would (a) test whether the O(1) scaling holds under scheduled access, (b) validate the analytical TDMA capacity formula (Eq. 12), and (c) provide a more credible coordinator bandwidth threshold. This single addition would substantially address the physical-layer abstraction concern.

3. **Run the uncapped sectorized mesh in the DES and report the overhead ratio as a function of N.** The analytical prediction is O(√N) growth in the overhead ratio, which would provide a much more informative comparison than the constant 2.2× from the capped variant. This would also demonstrate a case where the DES reveals behavior not trivially predictable from the analytical model (since the uncapped mesh may exhibit queueing effects at the sector coordinator level).

4. **Couple the AoI metric to a simplified conjunction detection model.** Even a simple model—e.g., "conjunction detection probability = f(AoI, orbital prediction error σ)"—would transform the AoI results from descriptive to prescriptive. This would allow the paper to make statements like "at p_exc = 0.10, conjunction detection probability drops below 95% for objects with σ > X km," which is directly actionable for mission design.

5. **Condense the paper by 20–25%.** The methodology section (III) and scaling results (IV-D) contain substantial redundancy. Table V (ten identical rows) can be replaced with a single statement. The analytical cross-check derivation (Section IV-D) can be shortened to a paragraph since the agreement is exact by construction. The freed space should be used for the TDMA model and uncapped sectorized mesh results suggested above.