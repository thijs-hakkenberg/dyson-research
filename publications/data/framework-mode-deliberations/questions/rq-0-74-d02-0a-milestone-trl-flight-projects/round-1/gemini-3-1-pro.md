---
questionId: "rq-0-74"
questionSlug: "d02-0a-milestone-trl-flight-projects"
modelId: "gemini-3-1-pro"
modelName: "Gemini 3.1 Pro"
roundNumber: 1
generated: "2026-10-17"
type: "discussion-response"
---

Here is the resolution for the application of D-02 to 0A flight projects, structured according to the Composite Scaffold.

### 1. Frame & decision type
**Frame:** The core conflict is a category error regarding reversibility. D-02 states "stringency follows reversibility." Claude argues a launch is a one-way gate, demanding TRL 6 at Preliminary Design Review (PDR). Gemini and GPT treat the Mid-Term Review (MTR) as a funding tranche release, accepting TRL 4–5. 
**Decision type:** Executive and property decision (amending/interpreting an accepted rule). 
**Domain:** Complicated (aerospace systems engineering). 
**Reversibility:** The policy decision is two-way (can be amended), but the physical act of launching a scout is one-way (irreversible capital expenditure and physical commitment).

### 2. Criteria and weights
Weights are assigned based on swing weight methodology (referencing the actual range of impact each criterion has on Phase 0A outcomes):
*   **C1: Programmatic Risk Alignment (Weight: High, 40%)** – The range spans from losing a scout vehicle due to immature tech (high cost/delay) to safely bounding risk. 
*   **C2: Schedule Velocity (Weight: Medium, 30%)** – The range spans from stalling early pathfinder flights while waiting for TRL 6, to rapid iterative testing.
*   **C3: Policy Consistency (Weight: High, 30%)** – The range spans from contradicting D-02's "stringency follows reversibility" to perfectly aligning program and project gates.

### 3. Options
*   **Option A: The Null / Tranche Approach (Gemini/GPT)** – Apply TRL 4–5 at the MTR for all 0A items. Flight readiness (TRL 8) is handled right before launch, but PDRs do not strictly require TRL 6. *Argument against: Ignores the irreversible nature of hardware commitment in flight projects.*
*   **Option B: Strict Flight Exemption (Claude)** – Scout and pathfinder critical technologies must be at TRL 6 at their own PDR. TRL 4–5 applies *only* to 0B development milestones. *Argument against: Over-constrains early agile scouts, treating them like flagship 0B missions.*
*   **Option C: Gate Stratification (Recommended)** – Distinguish between *Program* gates and *Project* gates. The 0A MTR (Program gate) requires TRL 4–5 to release the next tranche of funding. However, the specific Scout/Pathfinder PDR (Project gate) requires TRL 6 for its *own* flight-critical technologies before bending metal. 

### 4. Assessment matrix

| Option | C1: Risk Alignment | C2: Schedule Velocity | C3: Policy Consistency |
| :--- | :--- | :--- | :--- |
| **A (Null/Tranche)** | Low (Risks bending metal on TRL 4) | High (Fastest MTR pass) | Low (Violates reversibility principle for flights) |
| **B (Strict Exemption)** | High (Safest for flight hardware) | Low (Delays 0A flights significantly) | Medium (Creates a carve-out in D-02) |
| **C (Gate Stratification)**| High (Protects flight hardware) | Medium (Allows funding flow, paces hardware) | High (Resolves the paradox perfectly) |

### 5. Sensitivity vs trade-off points
*   **Sensitivity point:** C2 (Schedule Velocity) is highly sensitive to Option B. Forcing TRL 6 at the program MTR for flight projects could stall the entire 0A phase.
*   **Trade-off point:** We are trading off the administrative simplicity of a single MTR standard (Option A) against the physical reality of irreversible launch commitments (Option B/C). 

### 6. Evidence certainty
*   *Claim:* Launches are irreversible one-way doors requiring TRL 6 at PDR. 
    *   *Certainty (GRADE):* High. Standard NASA/ESA systems engineering practice (NPR 7123.1C) dictates TRL 6 by PDR for flight articles to bound cost/schedule risk.
    *   *Likelihood/Confidence (ICD 203):* Almost certain; High confidence.

### 7. Key assumptions
*   **Assumption 1:** Scout and pathfinder missions are funded out of the 0A budget tranches. 
    *   *Falsification:* If scouts are funded via a completely separate mechanism, the MTR criteria do not apply to them. (Least disconfirmed hypothesis: They are part of 0A).
*   **Assumption 2:** A scout failure is not a "project-ending" event for the *entire* Project Dyson, just for that specific scout.

### 8. Decision, warrant, accepted downside
**Y-Statement:** In the context of the Phase 0 TRL re-baseline, facing a conflict between program funding gates and flight project physics, we chose Option C (Gate Stratification), to achieve rapid funding release while preventing premature hardware fabrication, accepting the added administrative overhead of tracking project PDRs separately from the program MTR.

**Warrant (Toulmin):** Because "stringency follows reversibility" (D-02), and bending metal for a launch is irreversible, flight projects must hit TRL 6 at their specific PDRs; however, because the MTR is a two-way funding gate for the *program*, TRL 4–5 is sufficient at the MTR to authorize the work *toward* that PDR.

### 9. Consequences
*   **Enables:** The MTR can proceed without waiting for scouts to reach TRL 6.
*   **Constrains:** Scout projects cannot pass their own PDRs or begin final fabrication until their specific critical technologies reach TRL 6 in a relevant environment.
*   **Rule Text Update:** Amend D-02 interpretation to read: *"Two-way, internal 0A milestones (like MTR): TRL 4–5 is enough to release funding. However, any sub-project committing to irreversible flight hardware (scouts/pathfinders) must independently demonstrate TRL 6 at its own PDR."*