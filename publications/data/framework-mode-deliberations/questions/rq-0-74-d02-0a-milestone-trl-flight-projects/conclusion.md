---
questionId: "rq-0-74"
questionSlug: "d02-0a-milestone-trl-flight-projects"
type: "discussion-conclusion"
generatedBy: "gpt-6-1-sol"
generated: "2026-10-17"
framework: "18f503fe4ec6"
roundCount: 1
terminationReason: "unanimous-conclude"
---

## Summary

Claude Opus 5.5, Gemini 3.1 Pro and GPT-6.1 Sol converged on the central distinction: **TRL 4–5 at a reversible 0A funding milestone does not authorise a scout or pathfinder flight.** All three recommended separating programme tranche decisions from flight-project readiness decisions and preserving KDP-0B’s accepted requirement of TRL 6 in a relevant environment for project-ending technologies, without waivers. All three rejected leaving the present ambiguity unresolved, although reviewers criticised Gemini’s response for treating an active policy option as the null option.

The panel did **not** converge on the complete flight-project rule. Gemini proposed TRL 6 at each scout/pathfinder PDR for its flight-critical technologies. Claude and GPT distinguished flight-enabling functions from technologies carried as experiments, but proposed different experimental pathways: Claude specified TRL 5 at PDR plus targeted ground tests; GPT proposed an approved demonstration assurance case without a universal experimental TRL floor. Claude additionally proposed scout waivers and a programme-scale pathfinder threshold; those provisions did not gain panel-wide endorsement.

Claude and GPT explicitly recommended amending D-02 rather than relying on interpretation alone. Gemini proposed revised “interpretation” text. The shared actionable conclusion is therefore narrower than any complete draft: **clarify that gate stringency follows the commitment being authorised, not the Phase 0A label, while retaining an explicit owner decision on experimental technologies and exceptions.**

## Decision record

### Shared conclusion—not a fully agreed rule

**Models: Claude, Gemini and GPT.**

> In the context of D-01’s capability programme and D-02’s reversibility principle, facing ambiguity between 0A tranche releases and flight-project commitments, we chose to separate reversible funding milestones from flight-project readiness gates, to preserve development funding without treating MTR approval as flight authorisation, accepting additional project-level review and possible delays before irreversible commitments.

- **Warrant:** All three argued that the authorised commitment, rather than its phase label, determines the appropriate stringency.
- **Qualifier:** Their detailed definitions of flight-critical technologies and permissible exceptions differ.
- **Accepted downside:** Claude and GPT identified added assurance and classification work; Gemini identified the overhead of tracking programme and project gates separately.

### Position 1: Role-specific thresholds and explicit exceptions

**Model: Claude.**

> In the context of 0A funding both reversible development and irreversible flights, facing the need to protect missions without pre-empting experimental learning, we chose TRL 4–5 for tranche releases, TRL 6 at PDR for enabling technologies, and TRL 5 at PDR plus targeted tests for technologies under test, to protect minimum mission return while preserving learning tempo, accepting classification judgment and additional ground-testing cost.

- **Warrant:** Claude cited established technology-maturation practice, reported associations between immaturity and cost growth, and the distinction between enabling technologies and experimental subjects.
- **Qualifier:** Claude described the experimental TRL 5 floor and proposed 25% pathfinder budget threshold as engineering judgments with limited direct evidence.
- **Additional provisions:** Claude proposed owner-signed scout risk waivers and no waivers for enabling technologies at pathfinder PDR when the pathfinder exceeds the proposed programme-cost threshold.
- **Accepted downside:** Classification could be gamed; additional tests could cost time and money.

### Position 2: Programme/project gate stratification

**Model: Gemini.**

> In the context of programme funding decisions and flight-project commitments, facing conflicting interpretations of D-02, we chose TRL 4–5 at the MTR to fund development and TRL 6 at each scout/pathfinder PDR for its flight-critical technologies, to maintain funding flow while preventing premature hardware commitment, accepting separate programme and project gate administration.

- **Warrant:** Gemini argued that irreversible hardware commitments require greater maturity than reversible funding releases.
- **Qualifier:** Gemini did not articulate a separate pathway for experimental technologies.
- **Accepted downside:** Gemini accepted additional administration and pacing of flight hardware development.

### Position 3: Function-specific assurance without a universal experimental floor

**Model: GPT.**

> In the context of consequence-sensitive gates and a capability programme, facing ambiguity over 0A flight readiness, we chose reversible development releases, separate flight-enabling readiness requirements, and an independently reviewed experimental assurance pathway, to enable useful learning without weakening irreversible-commitment assurance, accepting governance overhead and explicit experiment-failure risk.

- **Warrant:** GPT argued that readiness must match the consequences of the authorised activity, not its phase label.
- **Qualifier:** Experimental failure must be bounded, interfaces and operations verified, and the learning case credible. Safety, licensing and KDP-0B requirements remain non-compensable.
- **Gate rule:** GPT proposed TRL 6 for flight-enabling critical technologies by PDR—or before an earlier irreversible implementation commitment—and applicable qualification, acceptance, integration and operational-readiness requirements before launch.
- **Accepted downside:** Added assurance work, possible PDR delays, and the possibility of less learning than planned.

## Decision-quality audit

### Round 1 — Claude response

- **Weakest links named in votes:** Claude named **information**; Gemini named **commitment**; GPT named **reasoning**.
- **Scaffold assessment:** Claude’s self-review and GPT’s review credited the criteria-first structure, genuine null option, explicit sensitivity analysis, calibrated evidence and falsifiable assumptions.
- **Unsupported or contested elements:** Claude acknowledged weak direct evidence for the experimental TRL 5 floor and 25% pathfinder threshold. GPT challenged Claude’s argument that requiring TRL 6 before a flight intended to establish TRL 7 is circular.
- **Values trade-offs identified by Claude:** Loss avoidance versus learning tempo; scout waiver flexibility versus auditability; and programme exposure sufficient to trigger stricter pathfinder treatment.
- **Voting outcome:** Claude and Gemini approved; GPT was neutral.

### Round 1 — Gemini response

- **Weakest links named in votes:** All three reviewers named **information**.
- **Missing or unsupported scaffold steps:** Claude and Gemini identified the absence of a genuine do-nothing/null option. Claude criticised the qualitative, unweighted assessment matrix, an assumption without a falsifier, and a sensitivity discussion that confused MTR and PDR. Claude and GPT challenged Gemini’s high-confidence inference from launch irreversibility to a universal TRL 6-at-PDR requirement.
- **Material omission identified by Claude and GPT:** Gemini did not distinguish experimental technologies from flight-enabling functions.
- **Values trade-off identified by Gemini:** Administrative simplicity and schedule velocity versus assurance before irreversible hardware commitments.
- **Voting outcome:** Claude and GPT rejected; Gemini was neutral.

### Round 1 — GPT response

- **Weakest links named in votes:** Claude named **reasoning**; Gemini named **alternatives**; GPT named **commitment**.
- **Scaffold assessment:** Claude and GPT credited the non-compensable requirements, genuine alternatives, calibrated evidence and assumptions with falsifiers.
- **Missing or unsupported elements:** Claude noted the absence of a quantified tipping point and reliance on a discretionary experimental assurance case rather than a numerical maturity floor. Gemini considered the alternatives insufficiently distinct.
- **Values trade-offs identified by GPT:** Learning versus mission-success assurance; additional ground maturation versus schedule; and one high-assurance pathfinder versus several cheaper experiments.
- **Voting outcome:** All three approved GPT’s response. This approval did not establish agreement on every proposed clause, given the substantive reservations and differing rules retained elsewhere.

## Key Points

- **MTR approval is not flight approval.** All three models supported this separation.
- **TRL 4–5 can apply to development of 0A flight technologies.** Claude’s revised position and GPT’s response did not restrict reversible tranche criteria solely to downstream 0B development; Gemini likewise allowed MTR funding toward flight-project PDR.
- **PDR readiness is a separate requirement.** All three supported TRL 6 at PDR for at least flight-enabling or flight-critical technologies; GPT would move that requirement earlier if irreversible implementation occurs earlier.
- **The experimental boundary is unresolved.** Claude and GPT supported distinguishing experiments from enabling functions; Gemini’s proposed rule did not make that distinction.
- **TRL 8 is not an agreed blanket pre-launch requirement.** Claude and GPT favoured qualification and acceptance language for the flight system rather than applying TRL 8 indiscriminately to experimental subjects.
- **KDP-0B remains unchanged.** All three retained TRL 6 in a relevant environment, without waivers, for project-ending technologies.
- **No shared numerical pathfinder exposure threshold emerged.** The 25% proposal came from Claude; GPT specifically questioned its justification.

## Unresolved Questions

1. **Which experimental readiness rule should govern?** Claude proposed TRL 5 at PDR plus tests; GPT proposed an assurance case without a universal floor; Gemini proposed TRL 6 for flight-critical technologies.
2. **How should dual-role technologies be classified?** Claude and GPT both warned against labelling mission-essential functions “experiments” to avoid assurance requirements.
3. **Are scout enabling-technology waivers permitted?** Claude proposed them; GPT’s drafted enabling-technology requirement contained no equivalent waiver; Gemini did not specify one.
4. **Does pathfinder programme exposure justify a special no-waiver gate?** Claude proposed a 25% budget trigger, but the panel did not endorse that threshold.
5. **Is an amendment necessary, or can binding existing standards support clarification?** Claude favoured amendment; GPT allowed that adequate existing standards could change that judgment; Gemini framed its update as interpretation.
6. **Which technologies need TRL 4 versus TRL 5 at the MTR?** The models’ shared gate separation does not settle the technology-by-technology scope in the background table.

## Recommended Actions

1. **Record the shared rule first.** Following all three models, state that reversible 0A tranche approval does not authorise irreversible flight implementation or launch.
2. **Draft an explicit D-02 update with unresolved clauses marked.** Following Claude and GPT, separate programme funding, flight-enabling readiness and experimental assurance; retain Gemini’s programme/project gate distinction without presenting the experimental rule as settled.
3. **Create a project-level technology–function–gate register.** Claude and GPT proposed recording technology roles, relevant environments and evidence; GPT additionally proposed recording the next authorised activity, expenditure exposure and failure disposition.
4. **Obtain an owner decision on the experimental pathway and exceptions.** The alternatives are Claude’s numerical floor and scout waiver provisions, Gemini’s flight-critical PDR threshold, and GPT’s bounded assurance-case pathway. Do not silently combine them into an agreed rule.
5. **Collect evidence that could change the ruling:**
   - **Claude:** rebooking/refund terms, demonstrated cheap and rapid reflight, ground-test costs, pathfinder budget concentration, and launch-window rigidity.
   - **GPT:** binding flight standards, procurement commitments, hazard and interface analyses, minimum useful mission return, and evidence that experimental failure still yields discriminating learning.
   - **Gemini:** confirmation of scout/pathfinder funding arrangements and the programme consequences of losing an individual scout.
6. **Update the decision and gate artefacts after owner resolution.** Claude and GPT proposed aligning `decisions.md`, the gate proposal and the TRL baseline; Claude additionally proposed project-specific flight-gate blocks.

```yaml
questionId: "rq-0-74"
topics:
  - id: programme-versus-flight-gates
    topic: Separate reversible tranche releases from flight authorisation
    positions:
      - statement: "TRL 4–5 may support reversible 0A funding releases, but separate flight-project readiness gates are required."
        models: ["Claude Opus 5.5", "Gemini 3.1 Pro", "GPT-6.1 Sol"]
        evidence: "All three invoke D-02's reversibility principle and distinguish MTR funding from irreversible flight commitments."
    resolution_status: resolved
    priority: critical
  - id: experimental-technology-readiness
    topic: Readiness requirements for technologies carried as experiments
    positions:
      - statement: "Require TRL 5 at PDR for technologies under test, with documented environments and targeted ground tests before CDR."
        models: ["Claude Opus 5.5"]
        evidence: "Claude distinguishes enabling technologies from experimental subjects, while acknowledging limited direct evidence for the TRL 5 floor."
      - statement: "Require TRL 6 at project PDR for scout and pathfinder flight-critical technologies."
        models: ["Gemini 3.1 Pro"]
        evidence: "Gemini cites aerospace maturation practice and irreversible hardware commitment; its response provides no separate experimental pathway."
      - statement: "Permit experimental technologies below flight-enabling thresholds under an approved, independently reviewed demonstration assurance case."
        models: ["GPT-6.1 Sol"]
        evidence: "GPT requires bounded failure effects, verified interfaces and operations, credible learning outcomes, and explicit acceptance of experiment-failure risk."
    resolution_status: open
    priority: critical
  - id: flight-enabling-gate-timing
    topic: Timing of flight-enabling maturity requirements
    positions:
      - statement: "Require TRL 6 for enabling technologies at project PDR."
        models: ["Claude Opus 5.5"]
        evidence: "Claude cites maturation practice and reported cost and schedule growth associated with immature technologies."
      - statement: "Require TRL 6 for flight-critical technologies at project PDR before irreversible hardware implementation."
        models: ["Gemini 3.1 Pro"]
        evidence: "Gemini distinguishes programme funding approval from project hardware commitment."
      - statement: "Require TRL 6 by PDR or before an earlier irreversible implementation commitment."
        models: ["GPT-6.1 Sol"]
        evidence: "GPT argues that procurement and other commitments may precede the milestone labelled PDR."
    resolution_status: partially-resolved
    priority: high
  - id: waivers-and-programme-exposure
    topic: Scout waivers and special pathfinder stringency
    positions:
      - statement: "Allow owner-signed scout enabling-technology waivers and apply no-waiver treatment to enabling technologies at pathfinder PDR above a proposed 25% share of the 0A budget."
        models: ["Claude Opus 5.5"]
        evidence: "Claude invokes cheap experimental opportunities and programme concentration, but labels the numerical threshold an owner value and engineering judgment."
      - statement: "The proposed experimental floor and mandatory 25% threshold need better justification."
        models: ["GPT-6.1 Sol"]
        evidence: "GPT's review identifies these provisions as reasoning weaknesses that could change with further justification."
    resolution_status: open
    priority: high
  - id: decision-text-change
    topic: Amendment versus interpretation of D-02
    positions:
      - statement: "Explicitly amend D-02 to remove the ambiguity."
        models: ["Claude Opus 5.5", "GPT-6.1 Sol"]
        evidence: "Both regard the flight-project and experimental distinctions as materially important additions; GPT would reconsider if binding existing standards already close the gap."
      - statement: "Update D-02's interpretation with programme and project gate text."
        models: ["Gemini 3.1 Pro"]
        evidence: "Gemini proposes revised interpretation text separating MTR funding from flight-project PDR."
    resolution_status: partially-resolved
    priority: medium
```