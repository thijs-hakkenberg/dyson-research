---
questionId: "rq-0-68"
questionSlug: "demand-gate-definitions"
modelId: "gemini-3-1-pro"
modelName: "Gemini 3.1 Pro"
roundNumber: 1
generated: "2026-10-17"
type: "discussion-response"
---

Here is the decision regarding the definitions of "within 3×" and "signed" for the demand gate (g-demand) at KDP-0B.

### 1. Frame & decision type
- **Frame:** Defining the specific pass/fail metrics for the 'g-demand' gate at KDP-0B to determine the scale of Phase 0B for Project Dyson.
- **Decision type:** Property/Executive decision (Kruchten). 
- **Reversibility:** One-way door (highly irreversible). KDP-0B releases significant capital; sizing the build incorrectly based on vague demand leads to stranded assets.
- **Cynefin domain:** Complicated. It requires expert systems engineering and programmatic governance to resolve.

### 2. Criteria and weights
*(Value-Focused Thinking, swing weights)*

1.  **Objectivity and Verifiability (Swing Weight: High, 40%)**
    *   *Why this weight fits the range:* The range goes from "subjective panel opinion" to "binary, auditable artifact." Because KDP-0B is a one-way gate for project-ending technologies, the gate must be objectively passable by an independent auditor.
2.  **Overproduction Risk Mitigation (Swing Weight: High, 40%)**
    *   *Why this weight fits the range:* The range goes from "sizing to speculative future demand" to "sizing strictly to committed demand." The primary purpose of D-01 sizing 0B by demand is to prevent overbuilding. 
3.  **Resolution of Circularity (Swing Weight: Low, 20%)**
    *   *Why this weight fits the range:* The range goes from "self-referential project promises" to "external legal/financial commitment." We must resolve Claude's valid flag that an internal project signing its own demand is circular, but this is a structural fix, not the primary economic driver.

### 3. Options
*(Including the null option and rejected options with arguments)*

- **Option A: Null / Status Quo (Leave split as is).** 
    *   *Argument for rejection:* As GPT noted, the gate is "not objectively passable" without defined terms. This guarantees a stalled KDP-0B review.
- **Option B: Timing-Only Reading (GPT's proposal).** "3×" means accepted date span ≤ 3× elapsed time from a common epoch. 
    *   *Argument for rejection:* Fails to constrain physical capacity (Overproduction Risk). Timing is important, but D-01 explicitly states demand *sizes* 0B. Sizing requires a quantity metric.
- **Option C: Quantity-Only Reading (Claude's proposal).** "3×" means signed annual demand is at least one third of nameplate output. "Signed" means funded Phase 1 line item or external offtaker.
- **Option D: Hybrid Synthesis (Selected).** 
    *   "3×" is a **Quantity** limit: Phase 0B nameplate capacity cannot exceed 3× the signed annual demand (e.g., if signed demand is 0.2 kt/yr, maximum 0B capacity is 0.6 kt/yr). 
    *   "Signed" means either a legally binding external offtaker agreement OR an internally funded Phase 1 line item. Both must include a product specification (T22), quantities, delivery node, and dated schedule.

### 4. Assessment matrix
*(QOC)*

| Option | Objectivity (40%) | Overproduction Risk Mitigation (40%) | Resolution of Circularity (20%) |
| :--- | :--- | :--- | :--- |
| **A: Null** | Fails | Fails | Fails |
| **B: Timing-Only** | Moderate | Fails | Moderate |
| **C: Quantity-Only** | High | High | High |
| **D: Hybrid Synthesis** | Very High | High | Very High |

### 5. Sensitivity vs trade-off points
- **Sensitivity point:** The definition of "signed" strongly affects Objectivity. If "signed" is allowed to mean a non-binding internal memo, Objectivity drops to zero and Overproduction Risk spikes.
- **Trade-off point:** Defining "3×" as a quantity multiplier trades away strict schedule bounding (timing) in favor of strict physical scale bounding (capacity). We accept this trade-off because physical capacity drives capital expenditure, which is the primary risk at KDP-0B.

### 6. Evidence certainty
*(GRADE, ICD 203)*
- **Claim:** Internal demand without a separately funded line item creates a circular justification loop that routinely leads to stranded aerospace assets. 
    *   *Certainty:* High confidence. (Based on standard systems engineering governance and historical major-program baseline failures).
- **Claim:** A 3× capacity-to-demand ratio provides sufficient margin for testing and scaling without authorizing unchecked overproduction.
    *   *Certainty:* Moderate confidence. (Dependent on specific process yields not yet validated at TRL 6).

### 7. Key assumptions
- **Assumption 1:** It is feasible to secure a funded Phase 1 line item or an external offtaker prior to KDP-0B (which only requires TRL 4-5 for internal milestones). 
    *   *Falsification:* Market analysis or internal budget cycles demonstrate that off-takers/sponsors require TRL 6+ demonstration *before* committing funds.
- **Assumption 2:** The product specification (T22) can be adequately defined at this phase to form a binding contract.
    *   *Falsification:* The relevant environment testing at TRL 6 alters the fundamental product characteristics, invalidating the signed spec.

### 8. Decision, warrant, accepted downside
*(Y-statement, Toulmin)*

**Decision:** In the context of the KDP-0B demand gate for Project Dyson, facing an ambiguous panel split on definitions, we chose Option D (Quantity limit of 3× capacity-to-demand, and "signed" requiring a funded line item/external contract with T22 specs), to achieve an objectively auditable gate that prevents overbuilding, accepting the downside that strict funding requirements may delay KDP-0B if external off-takers hesitate at early TRLs.

**Warrant:** Because D-01 dictates that demand sizes 0B, the metric must constrain physical capacity (quantity), and because Phase 1 is the same project, only external legal contracts or distinct, formally funded internal line items break the circularity of self-justification.

### 9. Consequences
- **Constrains:** Phase 0B design teams are now strictly constrained to a maximum nameplate capacity of 3× the explicitly funded/contracted demand. They cannot size the facility for "projected" or "hoped-for" demand.
- **Enables:** Allows the audit team to objectively pass or fail g-demand at KDP-0B by checking for two specific artifacts: a financial commitment document and a T22 specification sheet.
- **Follow-on decisions:** The project owner must now define the exact epoch and delivery window for the schedule component of the signed agreement.