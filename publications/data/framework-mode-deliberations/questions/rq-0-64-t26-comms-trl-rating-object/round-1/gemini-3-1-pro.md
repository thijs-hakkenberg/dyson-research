---
questionId: "rq-0-64"
questionSlug: "t26-comms-trl-rating-object"
modelId: "gemini-3-1-pro"
modelName: "Gemini 3.1 Pro"
roundNumber: 1
generated: "2026-10-17"
type: "discussion-response"
---

Here is the decision record for the T26 (deep-space communications and resilient command service) TRL rating object, structured according to the requested Composite Scaffold.

### 1. Frame & decision type
- **Frame**: We must define the assessed object for T26 to establish the baseline TRL, which dictates the funding and exit criteria for the KDP-0B gate. 
- **Decision type**: Executive and property decision (setting the standard for composite technologies). 
- **Reversibility**: Two-way door now, but becomes a one-way door once Phase 0A budgets and KDP-0B gate criteria are locked. 
- **Cynefin domain**: Complicated (requires expert analysis and systems engineering synthesis).

### 2. Criteria and weights
*Note: Weights are swing weights, representing the value of moving from the worst available outcome to the best available outcome on that specific criterion.*

1. **Risk Visibility at KDP-0B (Weight: 45%)**: The ability of the rating to force early retirement of integration and security risks. *Swing justification*: The gap between missing a project-ending architecture flaw (worst) and identifying it in Phase 0A (best) is the highest-impact variable.
2. **Alignment with NASA TRL Exit Criteria (Weight: 35%)**: Strict adherence to rating at the scale, environment, and duration required by the architecture. *Swing justification*: Deviating from standard TRL definitions introduces systemic programmatic risk, but is slightly less critical than actual physical/cyber risk visibility.
3. **Licensing & Regulatory Viability (Weight: 20%)**: Support for D-03 high-energy tug operations licensing. *Swing justification*: Command security will likely be a strict license condition, but the exact regulatory framework is still forming, making the swing slightly less impactful today than internal gate criteria.

### 3. Options
- **Null Option: Status Quo (Reject)**. Keep the divergent model ratings and defer the definition. *Argument against*: Fails to set a clear KDP-0B gate requirement, violating D-02.
- **Option 1: Rate Heritage Components (TRL 6-7)**. Assess T26 based on the maturity of its constituent parts (DSN, Mars Relay Network, standard CCSDS protocols). *Argument against*: Ignores the 2–4× node-count gap and the unproven key-management lifecycle in deep space.
- **Option 2: Rate Integrated Service (TRL 3-4)**. Assess T26 strictly as the integrated, authenticated fleet command service. Headline TRL is 3. 
- **Option 3: Rate Integrated Service as Headline, Publish Sub-ratings (TRL 3 / Sub 3-9)**. Assess the integrated service as TRL 3 (conditional 4), classifying it as an architecture-change risk, but explicitly publish the sub-ratings (RF heritage 9, DINET 7, authenticated fleet command 3) alongside it to isolate the funding requirement to the integration and authentication gaps.

### 4. Assessment matrix

| Option | 1. Risk Visibility (45%) | 2. TRL Rules Alignment (35%) | 3. Licensing Viability (20%) | Weighted Score |
| :--- | :--- | :--- | :--- | :--- |
| **Option 1 (Components)** | Low (Masks integration risk) | Low (Violates scale/environment rule) | Low (Fails to prove security) | 0.15 |
| **Option 2 (Integrated)** | High (Forces risk retirement) | High (Strict adherence) | High (Forces security proof) | 0.85 |
| **Option 3 (Hybrid)** | High (Forces risk retirement) | High (Strict adherence + nuance) | High (Forces security proof) | **0.95** |

### 5. Sensitivity vs trade-off points
- **Sensitivity point**: The decision is highly sensitive to the definition of "project-ending" in D-02. If unauthenticated command is deemed acceptable for early phases, Option 1 becomes viable.
- **Trade-off point**: We are trading off *Phase 0A cost/friction* (funding a breadboard path to TRL 6 for the integrated service) against *Phase 0B operational risk* (discovering at scale that post-outage key recovery fails). 

### 6. Evidence certainty
- **Claim**: Interplanetary RF links and conjunction operations are mature. 
  - *Certainty*: High confidence, virtually certain (IPCC). GRADE: High (extensive flight heritage).
- **Claim**: SDLS authenticated commanding with post-outage key recovery has not been demonstrated at the required fleet scale (15-29 assets).
  - *Certainty*: Medium confidence, likely (IPCC). GRADE: Moderate (absence of cited precedent, though classified precedents may exist).

### 7. Key assumptions
- **Assumption 1**: No existing mission has flown a fully integrated, multi-node SDLS authenticated command network with deep-space key recovery. 
  - *Falsification*: A cited deep-space flight record of this exact capability. (ACH: This hypothesis is currently the least disconfirmed).
- **Assumption 2**: High-energy tug operations will require cryptographic command assurance for licensing.
  - *Falsification*: A formal regulatory ruling stating standard unauthenticated CCSDS commands are sufficient for D-03 operations.

### 8. Decision, warrant, accepted downside
**Y-Statement**: In the context of the Phase 0 architecture re-baseline, facing divergent TRL assessments for deep-space communications (T26), we chose Option 3 (Rate Integrated Service as Headline TRL 3, Publish Sub-ratings), to achieve strict risk visibility at the KDP-0B gate while isolating the specific technology gaps, accepting the increased Phase 0A cost and schedule friction required to build and test an integrated breadboard.

**Toulmin Warrant**: Because NASA TRL exit criteria require assessment at the scale and environment the architecture demands, and because failure of authenticated command at scale is an architecture-changing (and potentially un-licensable) risk, the headline rating must reflect the lowest maturity of the critical integrated path (key management), not the highest maturity of its physical components.

### 9. Consequences
- **Constrains**: Phase 0A budget allocation. A funded path to TRL 6 (configuration-controlled integrated breadboard tested against predictions) must now be established for the authentication and integration elements of T26 before KDP-0B.
- **Enables**: Clear, targeted procurement for the T26 breadboard; establishes a precedent rule for all other composite technologies in the re-baseline (they must be rated as integrated articles, not by their best components).
- **Subsumes**: Resolves the GPT vs. Claude/Gemini divergence by adopting GPT's strict integrated rating object while preserving Claude's component nuance via sub-ratings.