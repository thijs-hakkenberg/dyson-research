---
questionId: "rq-0-72"
questionSlug: "composite-technology-trl-rule"
modelId: "gemini-3-1-pro"
modelName: "Gemini 3.1 Pro"
roundNumber: 1
generated: "2026-10-17"
type: "discussion-response"
---

Here is the structured decision for the headline TRL rule for composite technologies in Project Dyson, following the Composite Scaffold methodology.

### 1. Frame & decision type
*   **Decision Type:** Executive and property decision (Kruchten). It establishes a systemic rule for evaluating all composite technologies (propulsion, power, processing) against the KDP-0B gate criteria.
*   **Reversibility:** Two-way door during Phase 0A, but becomes a one-way door at KDP-0B due to the "no waivers" rule for project-ending technologies.
*   **Cynefin Domain:** Complicated. It requires expert engineering judgment but relies on established systems engineering heuristics.

### 2. Criteria and weights
*Value-Focused Thinking and Swing Weights applied before option generation.*
*   **C1: Gate Integrity & Strictness (Swing Weight: 100).** Range: From easily gamable to mathematically rigorous. Given D-02 bans waivers for project-ending technologies at KDP-0B, the rule must prevent premature advancement. Maximum weight applied.
*   **C2: Engineering Reality / Integration Fidelity (Swing Weight: 80).** Range: From ignoring integration interfaces to fully testing the composite in a relevant environment. System failures often occur at the interfaces of high-TRL components.
*   **C3: Reporting Clarity (Swing Weight: 40).** Range: From opaque single numbers to transparent sub-rating matrices. Important for stakeholder visibility but subordinate to actual technical readiness.

### 3. Options
*   **O1: Weakest Link Cap (Claude's position).** The headline TRL is strictly capped by the lowest TRL of any critical subsystem or component.
*   **O2: Integration-Specific Assessment with Critical Function Blockers (GPT's position).** The headline TRL is assessed based on the integration itself. However, an unvalidated critical function blocks the system claim. It does not automatically inherit the lowest sub-rating if that sub-rating's function is abstracted or mitigated in the specific integration.
*   **O3: Null Option / Case-by-Case (Status Quo).** Leave the panel's split unresolved and adjudicate each composite technology individually, as was done in the T26 (rq-0-64) ruling. *Rejected:* Fails C1 (Gate Integrity) by introducing massive administrative overhead and inconsistency at KDP-0B.

### 4. Assessment matrix
*(QOC: Options × Criteria)*

| Option | C1: Gate Integrity (100) | C2: Engineering Reality (80) | C3: Reporting Clarity (40) |
| :--- | :--- | :--- | :--- |
| **O1: Weakest Link Cap** | **High.** Mathematically prevents premature gate passage. | **Medium.** Ignores integration complexity (two TRL 6 parts might integrate at TRL 3). | **High.** Very easy to report and audit. |
| **O2: Integration Assessment** | **Medium.** Requires strict definitions of "critical function" to prevent gaming. | **High.** Accurately reflects that integration is a distinct engineering challenge. | **Medium.** Requires narrative justification alongside the number. |
| **O3: Null / Case-by-Case** | **Low.** Vulnerable to subjective waivers disguised as assessments. | **Medium.** Depends entirely on the specific review board. | **Low.** Inconsistent reporting across work packages. |

### 5. Sensitivity vs trade-off points
*   **Sensitivity Point (ATAM):** The definition of a "critical" component strongly affects C1 (Gate Integrity). If non-critical components are allowed to drag down the headline TRL, the project stalls; if critical components are misclassified as non-critical, the gate is breached.
*   **Trade-off Point (ATAM):** O1 vs O2 represents a trade-off between mechanical strictness (O1) and engineering accuracy (O2).

### 6. Evidence certainty
*   *Claim:* System integration often possesses a lower maturity than its constituent parts. **Certainty (GRADE): High.** (Well-documented in aerospace systems engineering literature; NASA Systems Engineering Handbook).
*   *Claim:* A mechanical "weakest link" rule prevents KDP-0B gate breaches. **Certainty (GRADE): Moderate.** (It prevents component-driven breaches, but does not inherently protect against integration-driven breaches if the weakest link is TRL 6 but the integration is untested).

### 7. Key assumptions
*   *Assumption 1:* We can accurately and objectively define which sub-components are "critical" (project-ending) versus substitutable.
    *   *Falsification (ACH):* If a component deemed "substitutable" fails and causes a schedule slip exceeding the Phase 0A buffer, the assumption is falsified.
*   *Assumption 2:* The T26 ruling (TRL 3, 4 conditional) implies a preference for integration assessment over mechanical capping.
    *   *Falsification (ACH):* If the owner clarifies that T26 was capped *specifically* because of its weakest link, rather than its integration state, this hypothesis is disconfirmed.

### 8. Decision, warrant, accepted downside
**Y-Statement:** In the context of the Phase 0 TRL re-baseline and the strict KDP-0B gate, facing a panel split on composite TRL calculation, we chose a **Hybrid Rule (Headline = min(Integration TRL, Lowest Critical Sub-component TRL))**, to achieve absolute gate integrity while respecting integration physics, accepting the heavier documentation burden required to prove integration TRL.

**Toulmin Argument:**
*   **Claim:** Composite TRL must be the lesser of the weakest critical component *or* the integration itself.
*   **Grounds:** D-02 bans waivers for project-ending technologies at KDP-0B.
*   **Warrant:** A system cannot operate in a relevant environment (TRL 6) if a critical piece of it cannot, nor can it operate if the pieces cannot work together. Therefore, both Claude's cap and GPT's integration assessment are necessary, not mutually exclusive.
*   **Qualifier:** This applies strictly to *critical* (project-ending) components.
*   **Accepted Downside:** Increased scrutiny and testing requirements for interfaces.

### 9. Consequences
*   **Constrains:** All work packages (WP-A, propulsion, power, processing) must now report a tripartite TRL: `[Integration TRL, Lowest Critical Component TRL, Headline TRL (Minimum of the two)]`.
*   **Enables:** Clear, un-gamable progression toward KDP-0B.
*   **Subsumes:** The T26 ruling is retroactively justified under this rule (the integration itself lacked a validated article, capping it at 3/4 regardless of component TRLs).