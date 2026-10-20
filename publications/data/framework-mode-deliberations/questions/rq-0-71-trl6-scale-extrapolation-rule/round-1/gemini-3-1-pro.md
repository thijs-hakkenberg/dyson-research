---
questionId: "rq-0-71"
questionSlug: "trl6-scale-extrapolation-rule"
modelId: "gemini-3-1-pro"
modelName: "Gemini 3.1 Pro"
roundNumber: 1
generated: "2026-10-17"
type: "discussion-response"
---

# 1. Frame & decision type

**Frame:** We must determine the scaling rules for TRL 6 demonstrations at KDP-0B for Project Dyson. Specifically, whether to enforce a fixed scale-extrapolation limit (e.g., $\le 10\times$) for throughput, power, and duration, or allow unlimited extrapolation justified by test-validated models. 
**Decision Type:** Executive and Property decision. It is a highly irreversible (one-way door) decision because it dictates the physical sizing, cost, and schedule of Phase 0 pathfinder facilities. 
**Cynefin Domain:** Complicated (expert engineering judgment and physics models are required to assess scaling laws).

# 2. Criteria and weights

*Swing weights are based on the actual range of variation between a massive, unaffordable MW-class pathfinder and a small, highly uncertain benchtop test.*

1.  **Pathfinder Cost & Feasibility (Weight: 40%)**: The difference between building a 100 kW pathfinder vs. a 1 MW pathfinder is hundreds of millions of dollars and years of facility construction. We must avoid mandating unaffordable ground tests.
2.  **Technical Risk Reduction / Scaling Confidence (Weight: 40%)**: The risk of non-linear physics (e.g., thermal runaway, plasma instabilities) dominating at larger scales. The weight reflects the existential threat to the project if a kt/yr facility fails due to unpredicted scaling effects.
3.  **Schedule / Time-to-KDP-0B (Weight: 20%)**: The time required to run duration tests. A strict limit on duration extrapolation (e.g., requiring 50% of life) could delay KDP-0B by years.

# 3. Options

*   **Option 1 (Null / Claude's proposal): Fixed $\le 10\times$ limit.** No more than 10× extrapolation in throughput or power, unless governing regimes are shown to be preserved. Duration can be met by partial test plus a validated wear model.
*   **Option 2 (GPT's proposal): No fixed limit.** No fixed acceptable scale factor in advance. Extrapolation must be justified entirely by test-validated models. Accelerated testing needs a validated degradation model.
*   **Option 3 (Hybrid / Regime-Preservation Rule): No fixed limit for throughput/power, fixed $\le 10\times$ limit for duration.** Power and throughput extrapolation have no fixed limit *if and only if* dimensionless parameters (e.g., Reynolds, Nusselt, Damköhler numbers) match the flight regime. Duration extrapolation is strictly capped at $10\times$ (i.e., minimum 10% life physical test) to anchor wear models.
*   **Rejected Option: Full-scale TRL 6 requirement ($1\times$ limit).** *Argument against:* MW-class or kt/yr ground facilities for space systems are financially and physically impossible within Phase 0 budgets.

# 4. Assessment matrix

| Criteria | Option 1 (Fixed $\le 10\times$ default) | Option 2 (No fixed limit) | Option 3 (Hybrid: Regime + Duration Cap) |
| :--- | :--- | :--- | :--- |
| **Pathfinder Cost** | Moderate to High (forces larger pathfinders if regime proof is hard) | Low (allows smaller pathfinders if models are trusted) | Low to Moderate (optimizes size, enforces duration) |
| **Scaling Confidence**| High (brute-force physical scale limits risk) | Low to Moderate (relies heavily on model accuracy) | High (anchors physics via dimensionless numbers, anchors wear physically) |
| **Schedule** | Moderate | Fast | Moderate (10% life test takes time) |

# 5. Sensitivity vs trade-off points

*   **Sensitivity Point:** The decision is highly sensitive to the *accuracy of multi-physics degradation models*. If our wear models are poor, Option 2 fails catastrophically.
*   **Trade-off Point:** Pathfinder Cost vs. Scaling Confidence. Option 2 maximizes cost savings but trades away physical scaling confidence. Option 1 maximizes confidence but drives up cost. Option 3 mediates this by splitting the physics (throughput/power) from the chemistry/mechanics (duration/wear).

# 6. Evidence certainty

*   *Claim 1:* Non-linear scaling effects in MW-class space power/propulsion often violate small-scale models. 
    *   **Certainty (GRADE):** Moderate.
    *   **Likelihood/Confidence (IPCC/ICD 203):** Very likely (90-100%); High confidence based on historical space nuclear and electric propulsion scaling failures.
*   *Claim 2:* Wear and degradation mechanisms (e.g., sputtering, creep) cannot be accurately modeled without at least 10% physical runtime.
    *   **Certainty (GRADE):** High.
    *   **Likelihood/Confidence:** Virtually certain (99-100%); High confidence. Standard aerospace practice (e.g., NASA EP qualification) requires extensive physical wear testing.

# 7. Key assumptions

*   **Assumption 1:** Dimensionless parameters for the target technologies can be fully matched at sub-scale.
    *   *Falsification:* If a technology requires matching both Froude and Reynolds numbers simultaneously in a 1g environment, sub-scale regime preservation is physically impossible.
    *   *ACH Ranking:* Hypothesis A (Regimes can be matched) is less disconfirmed than Hypothesis B (Regimes cannot be matched), assuming standard fluid/thermal systems, but requires case-by-case verification.
*   **Assumption 2:** 10% life testing is sufficient to capture late-in-life non-linear degradation.
    *   *Falsification:* Discovery of a wear mechanism (e.g., deep dielectric charging fatigue) that only initiates after 50% life.

# 8. Decision, warrant, accepted downside

**Y-Statement:** In the context of Project Dyson's Phase 0 to Phase 1 transition (KDP-0B), facing project-ending technologies requiring MW-class/kt-yr scales, we chose Option 3 (No fixed limit for power/throughput if governing regimes match; fixed $\le 10\times$ extrapolation limit for duration), to achieve affordable pathfinder sizing without sacrificing scaling confidence, accepting the schedule delay inherent in a minimum 10% life physical test.

**Warrant & Qualifier (Toulmin):** 
*   *Claim:* Option 3 provides the best balance of cost and risk.
*   *Grounds:* Physical scaling limits (Option 1) drive pathfinder costs beyond Phase 0 budgets, while purely model-based scaling (Option 2) introduces unacceptable risk for wear mechanisms.
*   *Warrant:* Because physics regimes can be mathematically proven to match at sub-scale using dimensionless numbers, but material wear over time is highly empirical and non-linear.
*   *Qualifier:* This holds true *provided* the technology's governing dimensionless parameters can actually be isolated and matched in a ground test facility.

# 9. Consequences

*   **Enables:** The immediate sizing and preliminary design of Phase 0 pathfinder facilities based on regime-matching rather than arbitrary scale factors.
*   **Constrains:** Forces the project to immediately begin long-duration life testing (minimum 10% of design life) to meet KDP-0B, constraining the Phase 0 schedule.
*   **Follow-on Decisions:** We must now define the specific "governing regimes" (dimensionless numbers) required for each project-ending technology, and establish the review board that validates these regime-preservation arguments.