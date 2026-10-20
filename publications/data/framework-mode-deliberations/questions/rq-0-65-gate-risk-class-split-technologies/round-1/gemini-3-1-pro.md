---
questionId: "rq-0-65"
questionSlug: "gate-risk-class-split-technologies"
modelId: "gemini-3-1-pro"
modelName: "Gemini 3.1 Pro"
roundNumber: 1
generated: "2026-10-17"
type: "discussion-response"
---

Here is the decision regarding the risk classification of the eight disputed technologies (T02, T10, T14, T15, T22, T24, T25, T26) for Project Dyson, structured according to the Composite Scaffold.

### 1. Frame & decision type
**Frame:** Executive and property decision. We must determine the gate stringency (Project-ending vs. Architecture-change) for eight disputed technologies at KDP-0B. 
**Reversibility:** Low (One-way door). Under-classing a technology allows KDP-0B to pass with unproven critical functions, risking catastrophic Phase 1 failure. Over-classing artificially lengthens Phase 0A.
**Domain:** Complicated (Cynefin), requiring expert systems engineering judgment to assess fallback viability.

### 2. Criteria and weights
*   **C1: Criticality to Core Autonomous Operations (Swing Weight: High).** The range spans from "mission fails entirely without it" to "mission degrades gracefully." High weight because Project Dyson's economics rely on remote/autonomous viability.
*   **C2: Viability of Fallbacks (Swing Weight: High).** The range spans from "no physical alternative exists" to "Earth-supply or standard COTS alternatives exist." High weight because the definition of "Architecture-change" requires a credible, costed fallback.
*   **C3: Phase 0A Schedule/Cost Impact (Swing Weight: Medium).** The range spans from "adds years to 0A" to "easily tested in 0A." Medium weight; schedule is important but secondary to avoiding unrecoverable KDP-0B commitments.

### 3. Options
*   **Option 1: The Null Option (Claude's Default).** Classify all 8 as *Project-ending*. Require TRL 6 in a relevant environment with no waivers at KDP-0B.
*   **Option 2: Split by Fallback Viability.** 
    *   *Project-ending:* T10 (Long-duration autonomy), T14 (Massive propellant storage), T24 (Dust-tolerant mechanisms), T25 (Target-local navigation). Argument: These are core to the novel operating environment; failure here means the mission cannot occur.
    *   *Architecture-change:* T02 (MW solar arrays), T15 (Site power), T22 (Product packaging), T26 (Deep-space comms). Argument: Fallbacks exist (smaller arrays, localized power, Earth-based packaging, standard DSN/commercial comms) that degrade economics but do not end the project.
*   **Option 3: All Architecture-Change (Rejected).** Argument for rejection: Pushes unacceptable technical risk past KDP-0B, violating the accepted D-02 principle that one-way gates need TRL 6 for project-ending tech.

### 4. Assessment matrix

| Option | C1: Core Criticality Risk | C2: Fallback Viability | C3: 0A Schedule Impact |
| :--- | :--- | :--- | :--- |
| **O1: Null (All Project-Ending)** | Lowest risk (forces proof) | Ignores viable fallbacks | Highest impact (lengthens 0A) |
| **O2: Split by Fallback** | Balanced risk | Accurately maps fallbacks | Moderate impact |
| **O3: All Arch-Change (Rejected)**| Unacceptable risk at 0B | Assumes fallbacks for all | Lowest impact (fast 0A) |

### 5. Sensitivity vs trade-off points
*   **Sensitivity point:** The viability of the fallback for T14 (Propellant storage). If hundreds of tonnes cannot be stored, the tug architecture fails. This is highly sensitive to C1.
*   **Trade-off point:** We are trading Phase 0A schedule velocity (which favors Architecture-change) against KDP-0B confidence (which favors Project-ending). 

### 6. Evidence certainty
*   **Claim:** T10, T14, T24, and T25 lack economically viable fallbacks. *Certainty: Moderate.* (Based on standard space mining/tug architectural studies; dust and autonomy are notoriously non-degradable risks).
*   **Claim:** T26 (Comms) has a viable fallback. *Certainty: High.* (Owner ruling rq-0-64 already leans this way; existing deep space networks can serve as a fallback, albeit at higher operational cost).

### 7. Key assumptions
*   **Assumption 1:** The fallbacks for T02, T15, T22, and T26 will not violate the economics required to pass the KDP-0B demand gate. *Falsification:* Phase 1 economic modeling shows that using standard solar arrays (T02 fallback) or Earth-packaging (T22 fallback) pushes the cost above the signed demand threshold.
*   **Assumption 2:** TRL 6 for T10 (Autonomy) and T24 (Dust) can be achieved in a "relevant environment" on Earth/LEO during Phase 0A. *Falsification:* Engineering teams prove that only lunar/asteroid surface testing can validate these, forcing a re-evaluation of 0A scope.

### 8. Decision, warrant, accepted downside
**Y-Statement:** In the context of the KDP-0B gate definition, facing a panel split on eight technologies, we chose Option 2 (Split by Fallback), to achieve a balanced Phase 0A schedule while protecting the one-way 0B gate, accepting the risk that fallbacks for the four Architecture-change technologies might degrade Phase 1 economics.

**Warrant (Toulmin):** Because Project-ending classification should be reserved for technologies without viable functional fallbacks (Grounds), and T02, T15, T22, and T26 have known, albeit less efficient, alternatives (Warrant), they can be safely classed as Architecture-change, provided the economic gate at 0B catches any cost overruns (Backing).

### 9. Consequences
*   **Enables:** Finalization of the WP-A TRL baseline and the KDP-0A review schedule.
*   **Constrains:** Phase 0A budget must now heavily prioritize reaching TRL 6 for T10, T14, T24, and T25, as they cannot be waived at KDP-0B.
*   **Follow-on decision:** The specific funded paths to TRL 6 for the four Architecture-change technologies (T02, T15, T22, T26) must be defined and costed before KDP-0A.