---
questionId: "rq-0-69"
questionSlug: "phase-0-sunset-rule"
modelId: "gemini-3-1-pro"
modelName: "Gemini 3.1 Pro"
roundNumber: 1
generated: "2026-10-17"
type: "discussion-response"
---

Here is the systems engineering assessment of the month-180 sunset condition for Project Dyson, structured via the Composite Scaffold.

### 1. Frame & decision type
- **Frame:** We must determine the authority and execution mechanism of the month-180 (M180) sunset clause for Phase 0. Specifically, whether reaching M180 without passing KDP-0B automatically triggers the fallback ("0A only, Earth supply"), or if M180 merely prompts a schedule review via rq-0-63.
- **Decision type:** Executive and property decision. It is a highly irreversible, one-way door decision (an automatic fallback commits the programme to a 15-year Earth-supply paradigm). 
- **Cynefin domain:** Complicated. The variables are known, but the interactions between schedule slips, option-keeping spend, and exogenous delays require expert analysis.

### 2. Criteria and weights
*Swing weights are based on the actual range of outcomes between a strict 15-year guillotine and an open-ended schedule.*

1. **Sunk-Cost Prevention (Weight: 80/100):** The ability of the rule to definitively cap Phase 0A spend and prevent "zombie" project drift. A 15-year (180-month) runway is already exceptionally long for a Phase 0 capability programme; the weight is high because the range between "capped at 15 years" and "indefinite extension" represents billions in potential sunk costs.
2. **Exogenous Shock Absorption (Weight: 40/100):** The programme's ability to survive delays outside its control (e.g., heavy-lift launch vehicle availability, geopolitical shifts). Weighted lower because a 180-month window already contains massive schedule margin.
3. **Schedule Integration (Weight: 60/100):** Alignment with the integrated schedule (rq-0-63). The rule must not create contradictory triggers where the system schedule allows a test, but the sunset clause forbids it.

### 3. Options
- **Option 0: Null (Status Quo / Keep the split).** Leave the panel's disagreement unresolved. *Rejected:* Fails to provide the owner with a clear gate condition for KDP-0B, guaranteeing a governance crisis at the first major schedule slip.
- **Option 1: Automatic Execution (Claude's position).** M180 is a hard sunset. Reaching M180 without clearing KDP-0B automatically triggers the "0A only, Earth supply" fallback. Caps 0A spend and prevents drift.
- **Option 2: Planning Boundary (GPT's position).** M180 is a planning boundary set via rq-0-63. It forces a review but is not authority for an automatic fifteen-year fallback commitment. Allows extensions for exogenous delays.

### 4. Assessment matrix (QOC)

| Option | Sunk-Cost Prevention (80) | Shock Absorption (40) | Schedule Integration (60) |
| :--- | :--- | :--- | :--- |
| **Option 0 (Null)** | Low (ambiguous) | High (de facto infinite) | Low (unresolved) |
| **Option 1 (Automatic)** | **High** (guaranteed cap) | Low (blind guillotine) | Medium (overrides rq-0-63) |
| **Option 2 (Boundary)** | Low (invites waivers) | **High** (human-in-the-loop) | **High** (driven by rq-0-63) |

### 5. Sensitivity vs trade-off points
- **Sensitivity point:** Option 1 is highly sensitive to *Sunk-Cost Prevention*. If the primary owner concern is runaway R&D budgets, Option 1 dominates.
- **Trade-off point:** There is a direct trade-off between *Sunk-Cost Prevention* (Option 1) and *Exogenous Shock Absorption* (Option 2). Enforcing a hard stop prevents budget drift but risks killing a viable architecture at month 179 due to a minor, external launch delay.

### 6. Evidence certainty
- *Claim:* A 180-month window is sufficient to absorb normal aerospace development delays without needing further extensions.
  - **Certainty:** Moderate (GRADE). 
  - **Likelihood:** Very Likely (>90% probability, IPCC) that 15 years is enough for Phase 0/TRL 6 maturation.
  - **Confidence:** High confidence (ICD 203) based on historical analogues (e.g., Apollo, ISS early phases) where fundamental architecture decisions were forced within a decade.

### 7. Key assumptions
*Evaluated using Analysis of Competing Hypotheses (ACH) principles.*

1. **Assumption:** An automatic trigger will actually be enforced by future stakeholders.
   - *Falsification:* Historical data showing that "automatic" cancellations in mega-projects are routinely overridden by political or owner waivers at the deadline.
2. **Assumption:** The integrated schedule (rq-0-63) cannot effectively cap costs without an external sunset clause.
   - *Falsification:* Evidence that rq-0-63 contains hard funding gates that automatically zero out budgets upon milestone failure.
   - *ACH Ranking:* The hypothesis that "human-in-the-loop boundaries lead to sunk-cost drift" is the *least disconfirmed* by historical aerospace systems engineering data.

### 8. Decision, warrant, accepted downside
**Y-Statement:** In the context of the Phase 0 TRL re-baseline, facing a panel split on the M180 sunset condition, we chose **Option 1 (Automatic Execution)**, to achieve definitive sunk-cost prevention and bound the KDP-0B real option, accepting the downside that a viable but delayed project might be forced into the Earth-supply fallback due to exogenous shocks near the deadline.

**Toulmin Argument:**
- **Claim:** The M180 sunset must automatically trigger the fallback.
- **Grounds:** 180 months (15 years) provides excessive schedule margin for reaching TRL 6 in a relevant environment.
- **Warrant:** Because mega-projects inherently resist cancellation once capital is deployed, only pre-committed, automatic structural guillotines can successfully terminate failing developmental pathways.
- **Qualifier:** Unless a catastrophic, non-project-related exogenous shock (e.g., global launch stand-down) occurs, which would require an extraordinary owner-level D-03 decision to pause the clock.

### 9. Consequences
- **Constrains:** The integrated schedule (rq-0-63) must now be built backwards from a hard M180 deadline. No internal 0A milestones can be planned beyond M150 to allow for the 36-month scout wave.
- **Enables:** Provides financial stakeholders with a guaranteed maximum exposure duration for the Phase 0 capability programme.
- **Subsumes:** This decision subsumes the KDP-0B slip rule (Claude's "One slip inside the month-180 sunset, then fallback" is now structurally enforced).