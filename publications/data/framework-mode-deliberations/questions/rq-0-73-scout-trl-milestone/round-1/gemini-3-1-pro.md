---
questionId: "rq-0-73"
questionSlug: "scout-trl-milestone"
modelId: "gemini-3-1-pro"
modelName: "Gemini 3.1 Pro"
roundNumber: 1
generated: "2026-10-17"
type: "discussion-response"
---

Here is the decision analysis for the rendezvous scouts and sampling payload TRL milestone, structured according to the Composite Scaffold.

### 1. Frame & decision type
**Frame:** This is an executive and property decision within a complicated domain (Cynefin). We must define the Technology Readiness Level (TRL) and schedule milestone for the rendezvous scouts (T11) and their subsurface sampling payloads (T18) during Phase 0A. 
**Reversibility:** Low (One-way door). Setting this gate dictates the schedule, funding profile, and launch cadence for Phase 0A. 

### 2. Criteria and weights
*Value-Focused Thinking applied via swing weights.*
*   **C1: Epistemic Rigor of the Target Gate (Weight: 40%)** - The degree to which the scout's data can be trusted to trigger KDP-0B. *Swing rationale:* The range goes from "unverified data" to "fully validated in-situ assay." High weight because the entire purpose of Phase 0A is to buy down risk for Phase 1.
*   **C2: Alignment with Standard Aerospace TRL Definitions (Weight: 35%)** - *Swing rationale:* Ranges from "redefining TRLs to fit our schedule" to "strict adherence to NASA/ESA definitions." High weight to prevent semantic drift where TRL 8 is demanded before a system has ever flown.
*   **C3: Schedule Feasibility (Weight: 25%)** - *Swing rationale:* Ranges from "impossible to meet without a time machine" to "achievable within 0A timelines." Moderate weight; we cannot mandate a schedule that physics or procurement prohibits.

### 3. Options
*   **O1: Null Option (Leave the panel split).** *Rejected.* Leaves the project without a verifiable gate for its most critical early hardware.
*   **O2: Claude's Position (TRL 6 at PDR).** Treats TRL 7-8 as the *result* of the scout mission. *Rejected as incomplete.* While accurate for the spacecraft build phase, it fails to define the requirement for the *Target Gate* itself.
*   **O3: GPT's Position (TRL 8 before launch, TRL 6 at KDP-0B).** *Rejected.* Demanding TRL 8 (flight qualified through test and demonstration) *before* the first scout launch conflates qualification with flight provenance. 
*   **O4: Synthesis Position (TRL 6 at Scout PDR; TRL 7 at Target Gate).** The scouts must reach TRL 6 (system/subsystem model or prototype demonstration in a relevant environment) to pass PDR and authorize flight build. To pass the *Target Gate* and trigger KDP-0B, the sampling payload (T18) must achieve TRL 7 (system prototype demonstration in an operational space environment) by successfully assaying the target.

### 4. Assessment matrix

| Option | C1: Epistemic Rigor | C2: TRL Alignment | C3: Schedule Feasibility |
| :--- | :--- | :--- | :--- |
| **O1 (Null)** | Low | Low | High |
| **O2 (Claude)** | Low (at Target Gate) | High | High |
| **O3 (GPT)** | High | Low (Misuses TRL 8) | Low |
| **O4 (Synthesis)** | High | High | Medium |

### 5. Sensitivity vs trade-off points
*   **Sensitivity point:** The definition of "relevant environment" for T18 (sampling) at TRL 6. If Earth-based vacuum/regolith chambers cannot adequately simulate the target asteroid's microgravity, C1 (Epistemic Rigor) drops sharply.
*   **Trade-off point:** We are trading early schedule velocity (allowing the scout to launch at TRL 6/7) against the risk of in-flight failure, to avoid the impossible standard of achieving TRL 8 before the first flight.

### 6. Evidence certainty
*   *Claim:* TRL 7 requires demonstration in an operational space environment. *Certainty:* High (Standard NASA/DoD definitions).
*   *Claim:* TRL 8 cannot be achieved prior to the first launch of a novel system. *Certainty:* High. TRL 8 requires actual flight qualification.

### 7. Key assumptions
*   **Assumption 1:** The target gate *requires* in-situ sampled grade evidence, not just remote sensing.
    *   *Falsification:* If remote sensing instruments are upgraded to provide bulk grade assay with high confidence, T18 physical sampling may not be project-ending.
*   **Assumption 2:** Phase 0A budget can absorb a scout failure and re-flight if the first scout fails to achieve TRL 7 in orbit.
    *   *Falsification:* If 0A only funds a single scout, the risk posture must shift to demand heavier Earth-based qualification (TRL 6+).

### 8. Decision, warrant, accepted downside
**Y-Statement:** In the context of Phase 0A target validation, facing a panel split on scout readiness levels, we chose **Option 4 (TRL 6 at PDR, TRL 7 at Target Gate)**, to achieve strict adherence to aerospace standards while ensuring rigorous evidence for KDP-0B, accepting the risk that the first scout launch acts as a TRL 7 technology demonstration rather than a fully mature operational asset.

**Warrant:** TRL definitions dictate that a system cannot reach TRL 7 or 8 without spaceflight. Therefore, demanding TRL 8 prior to launch (GPT) is impossible, but allowing the target gate to pass without operational demonstration (Claude's omission) is too risky. The scout *mission itself* bridges TRL 6 to TRL 7.

**Rule Text:** *"T11 (Rendezvous Scout) and T18 (Sampling Payload) must achieve TRL 6 (relevant environment demonstration) no later than Scout PDR. The Target Gate shall not be passed, nor KDP-0B triggered, until T18 achieves TRL 7 via successful in-situ operational demonstration on the target body."*

### 9. Consequences
*   **Constrains:** The Target Gate cannot occur until *after* the first scout has successfully landed, sampled, and assayed the target (achieving TRL 7).
*   **Enables:** Allows the scout engineering team to proceed to PDR with Earth-based vacuum/thermal testing (TRL 6), unblocking Phase 0A hardware development.