---
questionId: "rq-0-66"
questionSlug: "kdp-0b-trl6-scope-secondary-technologies"
modelId: "gemini-3-1-pro"
modelName: "Gemini 3.1 Pro"
roundNumber: 1
generated: "2026-10-17"
type: "discussion-response"
---

Here is the decision ruling on the KDP-0B TRL requirements for T11, T18, T09, T12, and T20, structured via the Composite Scaffold.

### 1. Frame & decision type
**Frame:** We must define the stringency of the KDP-0B gate for five disputed technologies. KDP-0B is a one-way door (committing to Phase 1 based on Phase 0 outcomes). 
**Decision Type:** Executive and property decision (setting the gate criteria). 
**Cynefin Domain:** Complicated. We are balancing the risk of premature commitment against the schedule cost of demanding TRL 6 for non-critical or self-proving systems.

### 2. Criteria and weights
Criteria are established before evaluating alternatives, using swing weights based on the actual range of impact at KDP-0B:
*   **C1: Risk Containment (Weight: 10/10).** The gate must prevent the project from proceeding if a true *project-ending* technology is unproven. The swing here is existential (project success vs. total failure).
*   **C2: Schedule Realism (Weight: 8/10).** The gate must not be artificially delayed by demanding TRL 6 for technologies that can be substituted or are proven in parallel flight. The swing is between a realistic KDP-0B date and a multi-year delay.
*   **C3: Architectural Flexibility (Weight: 6/10).** The ability to swap implementations (e.g., power tethers for beamed power) without failing the gate. 

### 3. Options
*   **O1: The Null Option (Status Quo).** Leave the panel split unresolved. *Rejected:* A gate cannot function with ambiguous criteria; KDP-0B would be unexecutable.
*   **O2: Strict TRL 6 (GPT's stance).** All five technologies (T11, T18, T09, T12, T20) must reach TRL 6 before KDP-0B. *Rejected:* T11 and T18 are 0A flight technologies; demanding TRL 6 *before* the gate ignores that their 0A flight *is* their maturation path. Demanding TRL 6 for T09/T12/T20 ignores that they are substitutable.
*   **O3: Tiered Exemption (Claude's stance).** T11 and T18 are classed as 0A flight technologies (exempt from the standard KDP-0B TRL 6 rule, as their maturity is settled by their scout missions). T09, T12, and T20 are classed as architecture-change (TRL ≥ 5 acceptable at KDP-0B with a waiver and a fully funded path to TRL 6).
*   **O4: Hybrid.** T18 (sampling) is deemed project-ending (TRL 6 required), T11 is 0A flight, and T09/T12/T20 are architecture-change. 

### 4. Assessment matrix

| Option | C1: Risk Containment (10) | C2: Schedule Realism (8) | C3: Arch. Flexibility (6) |
| :--- | :--- | :--- | :--- |
| **O1 (Null)** | Low | Low | Low |
| **O2 (Strict)** | High | Low (Forces massive delays) | Low (Locks in implementations) |
| **O3 (Tiered)** | Medium-High | High | High |
| **O4 (Hybrid)** | High | Medium | High |

### 5. Sensitivity vs trade-off points
*   **Sensitivity Point:** The classification of T18 (Subsurface sampling). If sampling is strictly required to validate the economic case at KDP-0B, then O3 fails C1.
*   **Trade-off Point:** We are trading absolute risk containment (O2) for schedule realism and architectural flexibility (O3). Demanding TRL 6 for distributed energy storage (T20) at KDP-0B would delay the gate for a system that can be substituted with centralized storage if necessary.

### 6. Evidence certainty
*   *Claim:* T09, T12, and T20 are architecture-change, not project-ending. **Certainty: High (GRADE).** There are known terrestrial and orbital fallbacks for power distribution and payload handling, even if less efficient.
*   *Claim:* T11 and T18 are 0A flight technologies. **Certainty: High.** Project Dyson's baseline funds 0A scout missions specifically to demonstrate these capabilities.

### 7. Key assumptions
*   **Assumption 1:** A waivered TRL 5 technology (T09, T12, T20) with a funded path to TRL 6 will not experience a fundamental physics failure in Phase 1. *Falsification:* Ground testing during Phase 0A reveals insurmountable environmental degradation (e.g., regolith shorting the high-voltage tethers).
*   **Assumption 2:** T18 (sampling) does not need to be TRL 6 *before* KDP-0B because the 0A scout flight will provide the necessary data. *Falsification:* The scout mission fails to launch before KDP-0B, leaving the economic gate without assay data.

### 8. Decision, warrant, accepted downside
**Y-Statement:** In the context of defining KDP-0B gate criteria, facing a panel split on five non-core technologies, we chose the Tiered Exemption (O3) to achieve schedule realism and architectural flexibility, accepting the risk that a waivered TRL 5 architecture-change technology might require an expensive Phase 1 redesign.

**Warrant:** KDP-0B is a gate to assess the viability of the project. Project-ending technologies must be TRL 6 because their failure ends the mission. Architecture-change technologies (T09, T12, T20) only degrade efficiency or require mass/cost penalties if they fail, which can be managed via waivers and funded maturation. T11 and T18 are self-proving via 0A flights; applying standard pre-gate TRL 6 rules to them creates a circular dependency.

### 9. Consequences
*   **Enables:** KDP-0B can be scheduled based on the maturation of the core 14 project-ending technologies, rather than waiting for tether (T09) or handling (T12) implementations to reach TRL 6.
*   **Constrains:** The Systems Engineering team must draft strict waiver conditions for T09, T12, and T20, defining exactly what constitutes a "funded path to TRL 6" and identifying the fallback architectures for each.
*   **Rule Text:** *"At KDP-0B, 0A flight technologies (T11, T18) are assessed via their mission data, not pre-gate TRL. Architecture-change technologies (T09, T12, T20) require TRL 6 in a relevant environment, OR TRL 5 with an approved waiver, a defined fallback architecture, and a fully funded Phase 1 maturation plan."*