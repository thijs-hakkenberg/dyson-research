---
questionId: "rq-0-67"
questionSlug: "economics-gate-capability-premium"
modelId: "gemini-3-1-pro"
modelName: "Gemini 3.1 Pro"
roundNumber: 1
generated: "2026-10-17"
type: "discussion-response"
---

### 1. Frame & decision type
This is an **executive and property decision** regarding the threshold criteria for the KDP-0B economics gate in Project Dyson. It is a **one-way door (highly irreversible)** decision, as passing KDP-0B commits the programme to Phase 1 execution based on signed demand. The decision operates in the **complicated** Cynefin domain, where expert analysis of cost models and governance structures is required. The core issue is whether a "capability premium" (R > 1) can be embedded as a passing condition within the gate itself, or if any cost exceeding Earth-supply parity requires an explicit, separate owner intervention.

### 2. Criteria and weights
Criteria are established prior to evaluating options, using swing weights based on the actual range of outcomes at KDP-0B.

*   **Governance Clarity & Accountability (Weight: 45%)**: The degree to which the decision forces explicit owner accountability for subsidies. *Swing rationale*: The difference between an automated gate pass at a $50B premium versus a forced owner signature is the largest governance delta in the programme.
*   **Cost Control & Robustness (Weight: 35%)**: Protection against the massive cost dispersion ($22–195B panel vs $15.7B BOM). *Swing rationale*: High weight due to the extreme variance in current estimates; the gate must prevent runaway capability subsidies.
*   **Strategic Capability Delivery (Weight: 20%)**: Alignment with D-01 (Phase 0 is a capability programme). *Swing rationale*: Lower weight because all options technically allow for capability delivery, they only differ on *how* it is authorized.

### 3. Options
*   **Option 1: Premium inside the gate (Claude's position)**. The gate passes if `0B P70 $/kg ≤ R × Earth-supply P50 $/kg`, where R > 1 is pre-set by the owner.
*   **Option 2: Parity at gate, premium requires separate decision (GPT's position)**. The gate threshold is strictly `Expected delivered cost ≤ Earth supply`. Any capability subsidy (R > 1) fails the standard gate and triggers a mandatory, explicit owner decision to proceed.
*   **Option 3: Undercut Earth supply (Gemini's position)**. The gate strictly requires `Delivered $/kg < Earth supply`. *Rejected* because it directly contradicts D-01 (capability programme, not cost saving).
*   **Option 4: Null option (Leave split as is)**. *Rejected* because an undefined gate criterion at KDP-0B prevents the establishment of a baseline and renders the economics gate un-executable.

### 4. Assessment matrix

| Option | Governance Clarity (45%) | Cost Control (35%) | Strategic Capability (20%) | Weighted Score |
| :--- | :--- | :--- | :--- | :--- |
| **1 (Premium in gate)** | Low (Subsidies hidden in R) | Medium (Capped by R) | High (Smooth pass) | 4.7 / 10 |
| **2 (Separate decision)** | High (Forces explicit sign-off) | High (Stops automatic overrun) | Medium (Adds friction) | **8.5 / 10** |
| **3 (Undercut)** | Medium | High | Low (Violates D-01) | *Rejected* |
| **4 (Null)** | Low | Low | Low | *Rejected* |

### 5. Sensitivity vs trade-off points
*   **Sensitivity point**: The decision is highly sensitive to the *launch-price scenario variance*. If Earth-supply costs drop significantly, Option 1's static R multiplier could inadvertently authorize massive absolute dollar subsidies.
*   **Trade-off point**: This is a classic trade-off between **governance friction** (Option 2 requires an extra executive loop) and **financial transparency** (Option 1 hides the subsidy in a pre-calculated gate metric).

### 6. Evidence certainty
*   **Claim**: There is massive cost dispersion in Phase 0 estimates.
    *   *Evidence*: Panel estimates $22–195B vs BOM $15.7B.
    *   *Certainty*: **High confidence** (ICD 203) that the uncertainty exists; **Very Likely** (>90% probability) that actual costs will deviate from the BOM.
*   **Claim**: Embedding R in the gate obscures the absolute cost of the capability premium.
    *   *Evidence*: Basic arithmetic of relative multipliers (R) applied to fluctuating baselines (Earth supply).
    *   *Certainty*: **High confidence**.

### 7. Key assumptions
*   **Assumption 1**: Earth-supply P50 $/kg can be accurately modeled at KDP-0B.
    *   *Falsification*: Radical market disruption (e.g., Starship achieving full, rapid reusability earlier than projected) making Earth-supply costs highly volatile and unpredictable.
*   **Assumption 2**: The owner is available and willing to make a separate capability subsidy decision at KDP-0B.
    *   *Falsification*: Owner delegates all KDP-0B authority to a steering committee that lacks the mandate to authorize budget overruns.
*   **ACH Ranking of Hypotheses regarding D-01**:
    1.  *Least disconfirmed*: D-01 means we *can* pay a premium, but we must know exactly what we are paying (supports Option 2).
    2.  *More disconfirmed*: D-01 means the premium is pre-approved as a structural project metric (Claude's view; disconfirmed by the need for strict KDP-0B financial controls).

### 8. Decision, warrant, accepted downside
*   **Y-Statement**: *In the context of* the KDP-0B economics gate, *facing* extreme cost estimate dispersion ($15.7B to $195B), *we chose* Option 2 (Cost parity as the gate threshold, with any premium requiring a separate owner decision), *to achieve* explicit executive accountability for capability subsidies, *accepting* the added governance friction of a potential two-step approval process at the gate.
*   **Warrant (Toulmin)**: Because Phase 0 is a capability programme (D-01), a premium is permissible; however, because the cost dispersion is dangerously wide, embedding a static multiplier (R) inside an automated gate risks authorizing unaffordable absolute dollar subsidies without executive oversight. Therefore, the gate must test for parity, and the premium must be an explicit executive exception.
*   **Qualifier**: This holds true provided Earth-supply costs do not drop so low that parity becomes physically impossible for space-based supply under any physics-based model.

### 9. Consequences
*   **Constrains**: The systems engineering team cannot "design to R" as a guaranteed passing metric; they must design to Earth-supply parity or prepare a rigorous justification for the subsidy.
*   **Enables**: Enables the owner to dynamically assess the value of the capability premium at the exact moment of the KDP-0B decision, using the most up-to-date Phase 1 signed demand.
*   **Follow-on decisions**: Requires the creation of a standardized "Capability Premium Justification" template to be used if the economics gate fails but the technical gates pass.