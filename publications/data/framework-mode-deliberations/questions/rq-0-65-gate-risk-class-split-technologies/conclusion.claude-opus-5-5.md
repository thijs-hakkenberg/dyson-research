---
questionId: "rq-0-65"
questionSlug: "gate-risk-class-split-technologies"
type: "discussion-conclusion"
generatedBy: "claude-opus-5-5"
generated: "2026-10-17"
framework: "18f503fe4ec6"
roundCount: 1
terminationReason: "unanimous-conclude"
role: "alternate synthesis"
---

## Summary

All three models agreed that the owner should not settle the eight split technologies by counting votes. They differed on what should replace the vote.

- **Claude Opus 5.5 and GPT-6.1 Sol** each proposed a generating rule. Under it, a function is project-ending by default and moves to a lower class only when the owner accepts an independently reviewed fallback dossier or package. The fallback must keep 0B production viable.
- **Gemini 3.1 Pro** proposed a judgement-based split by fallback viability, with no generating rule. It made T02, T15, T22 and T26 architecture-change and T10, T14, T24 and T25 project-ending.
- **No model re-ruled T26.** All three kept the owner's architecture-change ruling from rq-0-64. Claude offered its rule to rq-0-64 as the test. GPT made the ruling time-bounded, with automatic elevation to project-ending at KDP-0A unless survivable substitution is shown.

The main disagreement between Claude and GPT is the *current* status of T14, T24, T25 and the productivity part of T10.

- **Claude** ruled T14, T24, T25 and T10b architecture-change now, "provisional on dossiers". It kept T02, T10a, T15 and T22 project-ending.
- **GPT** ruled all seven non-T26 items project-ending until fallback evidence exists.
- **The votes** (Claude's self-vote and GPT's vote on Claude) noted that Claude's table contradicts its own rule. Under CR-1, a function is project-ending until a dossier is accepted, and none yet exists. Applying CR-1 as written would give GPT's interim classifications.

Gemini's per-technology split is the opposite of Claude's on several items. Claude's and GPT's votes both rejected it, on the grounds that its fallbacks were asserted without evidence and that it relied on the economics gate as a backstop. Gemini nonetheless voted to approve both Claude's and GPT's responses.

Convergence is therefore partial. Claude and GPT, with approving votes from Gemini, agree on the form of the rule: project-ending by default, reclassification on an independently reviewed fallback, and attention to common-cause failure. They also agree on the T26 handling. Interim classifications are not converged. The most supported interim reading in the votes is GPT's, but Claude's response as written and Gemini's response both differ from it.

## Decision record

The panel converged only partly, so this section gives the shared core first and then one Y-statement per position.

**Converged core (Claude and GPT; Gemini approved both responses in voting):**

- Adopt a rule under which a technology function is project-ending at KDP-0B unless the owner accepts an independently reviewed fallback package. The package must show that the fallback preserves authorised 0B production, is not common-cause with the primary, and closes within the approved limits.
- Until a package is accepted, the function requires TRL 6 in a relevant environment, with no waiver.
- T26 keeps the architecture-change ruling from rq-0-64.
- Warrant (both): stringency follows reversibility (D-02). Failure consequence, not vote counts or current TRL, sets the assurance required.

**Position 1: evidence-conditioned, seven project-ending, T26 bounded (GPT-6.1 Sol).**
In the context of a funded 0A capability programme and an optional 0B production commitment, facing unresolved classifications and unevidenced fallbacks, we chose project-ending for T02, T10, T14, T15, T22, T24 and T25, and a time-bounded architecture-change ruling for T26 that elevates automatically at KDP-0A without evidence, to protect the irreversible investment while permitting demonstrated substitution, accepting additional 0A qualification effort and a possibly delayed or rejected 0B.

- *Warrant:* indispensable production functions need demonstrated capability before commitment.
- *Qualifier:* the classes are revisable on architecture-specific evidence.
- *Rebuttal:* if fallback claims cannot be independently reviewed, the safer policy is permanent project-ending for all eight (GPT's option B).

**Position 2: CR-1 at function level with provisional downgrades (Claude Opus 5.5, as written).**
In the context of the Phase 0 TRL re-baseline under D-01 and D-02, facing a three-model split driven mostly by inconsistent scope and definitions, we chose rule CR-1 (project-ending unless a fallback dossier shows TRL ≥ 5, estimate class ≤ 4, an economics-gate pass with TRL-evidenced inputs, no common cause, and schedule within tolerance), applied at function level, to achieve protection against irreversible commitment without lengthening 0A for functions with real fallbacks, accepting that T02 and possibly T10b may be held at TRL 6 longer than necessary, and that the rule's safety depends on independent dossier review.

- *Interim rulings:*
  - Project-ending: T02, T10a, T15, T22.
  - Architecture-change, provisional: T10b, T14, T24, T25.
  - T26 unchanged.
- *Qualifier:* probably right for T02, T15, T22 and T10a; provisional for T14, T24 and T25.
- *Rebuttal:* if the economics model cannot price fallback branches, revert to the null option.
- *Caveat from the votes (Claude self-vote; GPT on Claude):* the interim downgrades contradict CR-1's own default.

**Position 3: split by fallback viability (Gemini 3.1 Pro).**
In the context of the KDP-0B gate definition, facing a panel split on eight technologies, we chose to make T10, T14, T24 and T25 project-ending and T02, T15, T22 and T26 architecture-change, to achieve a balanced 0A schedule while protecting the one-way gate, accepting that the fallbacks for the architecture-change items might degrade Phase 1 economics.

- *Warrant:* project-ending should be reserved for technologies with no viable functional fallback.
- *Backing:* the economics gate at 0B catches cost overruns.
- *Caveat from the votes:* Claude and GPT both voted to reject. They said the fallbacks are unevidenced and that relying on the economics gate conflicts with D-02.

## Decision-quality audit

| Response (Round 1) | Votes | Weakest link named | Scaffold steps missing or unsupported |
|---|---|---|---|
| **Claude Opus 5.5** | Gemini approve; Claude neutral; GPT neutral | Reasoning (Claude self-vote); commitment (GPT) | **Step 8:** per-technology rulings for T14, T24, T25 and T10b contradict CR-1's project-ending default. **Step 4:** arithmetic slips noted in Claude's self-vote (option A should be 3.2, not 3.30; option E 3.0, not 3.10). The slips do not change the ranking. **Step 8 (self-consistency):** Claude itself flags its earlier T25 inconsistency between the class table and the disputed list, and resolves it toward GPT's earlier view. |
| **Gemini 3.1 Pro** | Claude reject; GPT reject; Gemini neutral | Information (all three votes) | **Step 2:** weights given only as High/Medium, with no swing ranges. **Step 4:** qualitative matrix with no scores. **Step 6:** certainty rests on unnamed "standard studies". T26 is given "High" certainty although the owner ruling reads "possibly project-ending". **Step 7:** no analysis of competing hypotheses on why the panel split (Gemini self-vote). **Step 3:** the null option is framed as all eight project-ending, which includes T26 against the rq-0-64 ruling. **Step 8:** the warrant relies on the economics gate, which the Claude and GPT votes say conflicts with D-02. |
| **GPT-6.1 Sol** | Claude approve; Gemini approve; GPT approve | Alternatives (Claude); information (GPT self-vote) | **Step 4:** arithmetic slips noted by Claude's vote (option B should be 3.4, option D 2.35). The slips do not change the ranking. **Step 3:** options B and C differ mainly in the reclassification path (Claude's vote). **Step 8:** does not split T10 into functions, although it endorses splitting IDs "where necessary". **Step 6:** acknowledges that no test reports or costed fallback studies were in the record. |

**Divergences that are trade-off points (values questions), not facts to settle:**

- **Direction of the burden of proof.** Claude and GPT default to project-ending. Gemini assigns the class on a judgement of fallback viability. Claude calls this an owner judgement on appetite for 0A delay versus 0B regret.
- **What "project-ending" ends.**
  - Claude: 0B production failing the economics gate, which Claude calls the broad reading.
  - GPT: the 0B production commitment, explicitly not the 0A programme.
  - Gemini: "mission cannot occur", which is closer to the narrow reading.
- **Whether degraded-throughput 0B counts as a fallback** (Claude), and **how much production reduction is acceptable** (GPT). This is linked to D-01's demand sizing.
- **0A schedule velocity versus KDP-0B confidence.** All three named this trade-off.
- **Staffing and recurring communications cost versus autonomy** (GPT).

**Divergences that are facts to settle (sensitivity points named by the models):**

- Economics-model sensitivity to available power, for T02 and T15 (Claude).
- Propellant selection, cryogenic-only or with a storable branch, for T14 (Claude; Gemini named T14's fallback as its key sensitivity).
- Round-trip light time to the selected target, for T10 (Claude), and disconnected endurance, for T10, T25 and T26 (GPT).
- Spares mass fraction versus mean time between failures from life tests, for T24 (Claude), and the maintenance concept (GPT).
- Whether the SEL1 node is a cooperative target, for T25 (Claude).
- The signed buyer product specification, for T22 (Claude and GPT).
- Common-cause independence of fallbacks (Claude and GPT).

## Key Points

1. **Claude and GPT both proposed a generating rule with project-ending as the default.** Gemini's per-item judgement drew two rejecting votes.
2. **Claude's ACH analysis attributes the panel split mainly to scope (H-scope) and definition (H-definition), not technical disagreement.**
   - Its examples: T26's TRL 3 versus 7 reflects "link" versus "service"; T02 carries a "tug; site" annotation; T10 covers functions with different consequences.
   - GPT similarly said T26's spread needs a common unit of assessment.
   - GPT ranked "essential functions with potentially replaceable implementations" as the least disconfirmed hypothesis.
3. **Function-level splitting.** Claude proposed splitting T10 into T10a (safety-critical autonomy) and T10b (productivity autonomy), and folding T02 site arrays into T15. GPT endorsed splitting in principle without applying it to T10.
4. **Role of the economics gate.**
   - Claude: the economics gate cannot see technical immaturity (its option D, rejected). Fallback inputs to it must carry TRL evidence equal to the fallback's own and be reviewed independently.
   - GPT, in its vote: the economics gate cannot substitute for technical evidence.
   - Gemini relied on the economics gate as backstop.
5. **T26.** All three kept architecture-change. GPT added automatic elevation at KDP-0A. Claude offered CR-1 to rq-0-64 as the test: project-ending if no combination of DSN, ESA tracking and commercial ground service meets fleet command demand.
6. **Fallback admissibility.**
   - Claude: TRL ≥ 5, estimate class ≤ 4, economics pass, no common cause, schedule within tolerance.
   - GPT: an independently reviewed package with integrated budgets and transition resources. A fallback that needs an unqualified project-ending technology is inadmissible. "Use smaller arrays" alone is not evidence.
7. **Source control (GPT).** The "agreed core" project-ending list includes technologies whose individual panel classifications differ, for example T02. GPT recommends treating it as a proposed baseline, not as evidence of unanimity.
8. **Reliability of panel inputs (Claude).** Claude rated the panel TRL estimates as very low certainty and said they should not be used to set classes. GPT said the TRL spreads are not probability distributions.

## Unresolved Questions

1. **Interim class of T14, T24, T25 and T10b.** Should these be provisionally architecture-change (Claude as written) or project-ending until a dossier is accepted (GPT; CR-1 as written, per the votes)? For T14, T24 and T25, Gemini also says project-ending.
2. **T02, T15 and T22.** Claude and GPT say project-ending; Gemini says architecture-change. The question is whether any evidenced fallback exists.
3. **Definition of "project-ending".** Is it the broad reading (fails the economics gate) or the narrow one (programme cannot proceed)? Claude says this ruling would move T02 and T14.
4. **Splitting T10.** Should T10 be split into T10a and T10b, and should T02 site arrays be moved under T15?
5. **Whether the economics model can price fallback branches.** Claude's assumption A1 is untested. If it fails, Claude says CR-1 collapses toward the null option.
6. **T26 closure.** What test and deadline should apply, and does elevation happen automatically (GPT) or through the rq-0-64 process (Claude)?
7. **Re-elicitation.** Would re-elicitation with fixed scope still split? Claude says that if it did, structured expert elicitation (Cooke or SHELF) should replace rule-based inference.
8. **Status of the "agreed core" list** (GPT's source-control point).
9. **Relevant-environment testing for T10 and T24.** Gemini's assumption 2 asks whether TRL 6 can be shown on Earth or in LEO, or only at the target.

## Recommended Actions

1. **Owner:** rule on the form of the class rule. The candidates are Claude's CR-1 text or GPT's rule text; both default to project-ending and require independently reviewed reclassification. Record the definition of "project-ending" explicitly as a values ruling (Claude, GPT).
2. **Owner:** rule on interim classes for T14, T24, T25 and T10b, resolving the contradiction the votes found in Claude's table. Also rule on T02, T15 and T22, where Gemini dissents.
3. **WP-A:** decide whether to split T10 into T10a and T10b and whether to move T02 site arrays under T15 in `trl-baseline.yaml` (Claude). Fix a common unit of assessment for T26 (GPT).
4. **Technology leads:** produce fallback dossiers or packages as named 0A deliverables, with pass criteria (Claude, GPT):
   - T02: modular-array cluster.
   - T10b: supervised operations.
   - T14: storable or water branch.
   - T24: redundancy plus life tests.
   - T25: cooperative node with ground-in-the-loop navigation.
5. **Economics team:** add fallback branches with TRL-tagged inputs to the model, run the power and throughput sensitivity analysis, and audit whether fallback inputs dominate the outputs (Claude; Claude names this the most valuable 0A analysis for this question).
6. **Systems engineering:** make the propellant selection by KDP-0A, since it is on T14's critical path (Claude). Maintain dependency and common-cause analyses across power, autonomy, navigation and communications (GPT).
7. **Demand gate:** couple T22's TRL 6 definition to the signed buyer product specification (Claude, GPT).
8. **rq-0-64:** adopt a bounded T26 closure test with a KDP-0A deadline (GPT), using the fallback criterion as the test (Claude).
9. **Gate proposal:** correct the "agreed core" list so that it reads as a proposed baseline (GPT). Fix the arithmetic slips the votes identified in Claude's and GPT's matrices.

```yaml
questionId: "rq-0-65"
topics:
  - id: classification-method
    topic: Generating rule versus per-technology judgement
    positions:
      - statement: Adopt a generating rule; a function is project-ending unless an independently reviewed fallback dossier or package shows a credible, costed, non-common-cause fallback preserving viable 0B production
        models: [Claude Opus 5.5, GPT-6.1 Sol]
        evidence: Claude's ACH finding that the split is mainly scope and definition; auditability and repeatability for new items (T09, T12, T20, T18, T11); D-02 reversibility principle; GPT's argument that failure consequence, not vote counts, sets assurance
      - statement: Classify each technology by judgement of fallback viability, without a generating rule
        models: [Gemini 3.1 Pro]
        evidence: Named fallbacks (smaller arrays, localized power, Earth-based packaging, DSN or commercial comms); appeal to standard space mining and tug architecture studies
    resolution_status: partially-resolved
    priority: critical
  - id: interim-class-t14-t24-t25-t10b
    topic: Interim class of T14, T24, T25 and T10 productivity autonomy before dossiers exist
    positions:
      - statement: Architecture-change now, provisional on dossiers (T14 conditional on a storable propellant branch; T24 with life-test campaign; T25 with funded path to TRL 6; T10b on supervised-operations dossier)
        models: [Claude Opus 5.5]
        evidence: Credible priceable fallbacks (storable or water propellant, redundancy and replacement, Hayabusa2 and OSIRIS-REx single-craft navigation heritage, supervised operations); votes by Claude and GPT note this contradicts CR-1's own default
      - statement: Project-ending until a fallback package is accepted
        models: [GPT-6.1 Sol]
        evidence: No admissible fallback is demonstrated in the record; unproven alternatives do not justify lower classification
      - statement: T10, T14, T24 and T25 are project-ending because they are core to the novel operating environment
        models: [Gemini 3.1 Pro]
        evidence: Dust and autonomy described as non-degradable risks; failure means the mission cannot occur
    resolution_status: open
    priority: critical
  - id: class-t02-t15-t22
    topic: Class of T02 MW arrays, T15 site power and T22 product qualification
    positions:
      - statement: Project-ending
        models: [Claude Opus 5.5, GPT-6.1 Sol]
        evidence: T02 has the largest scale gap beyond ~100 kW-class flight heritage; T15 is common-cause with T02; T22 is required for buyer acceptance; 'smaller arrays' alone is not evidence
      - statement: Architecture-change
        models: [Gemini 3.1 Pro]
        evidence: Fallbacks (smaller arrays, localized power, Earth-based packaging) degrade economics but do not end the project; the economics gate catches overruns
    resolution_status: open
    priority: high
  - id: t26-handling
    topic: T26 classification and interaction with rq-0-64
    positions:
      - statement: Keep architecture-change; do not re-rule here; offer CR-1 to rq-0-64 as the test (project-ending if no combination of DSN, ESA and commercial service meets fleet command demand)
        models: [Claude Opus 5.5]
        evidence: Owner ruling is a must-criterion; T26's TRL spread reflects scope (link versus service)
      - statement: Keep architecture-change until KDP-0A; elevate automatically to project-ending unless survivable substitution or disconnection is demonstrated
        models: [GPT-6.1 Sol]
        evidence: T26 substitution has low certainty; it depends on service alternatives and evidence on disconnected operations
      - statement: Architecture-change, with a viable fallback held at high certainty
        models: [Gemini 3.1 Pro]
        evidence: Owner ruling leans this way; existing deep-space networks as fallback at higher operating cost
    resolution_status: partially-resolved
    priority: high
  - id: economics-gate-role
    topic: Whether the economics gate can backstop under-classed technologies
    positions:
      - statement: The economics gate cannot see technical immaturity; fallback inputs must carry TRL evidence and independent review
        models: [Claude Opus 5.5, GPT-6.1 Sol]
        evidence: Claude's rejection of option D and its premortem on optimistic productivity inputs; GPT's vote that the economics gate cannot substitute for missing technical evidence
      - statement: The economics gate at 0B catches cost overruns from architecture-change fallbacks
        models: [Gemini 3.1 Pro]
        evidence: Stated as backing in Gemini's Toulmin warrant
    resolution_status: open
    priority: high
  - id: project-ending-definition
    topic: What 'project-ending' ends
    positions:
      - statement: Broad reading; 0B production cannot meet the economics gate and signed demand
        models: [Claude Opus 5.5]
        evidence: D-01 sizes 0B on signed demand; Claude flags this as an owner values question
      - statement: Ends the 0B production commitment, not the 0A programme; '0A only, Earth supply' is an exit, not a fallback
        models: [GPT-6.1 Sol]
        evidence: D-01 real-option structure
      - statement: Mission cannot occur without the technology
        models: [Gemini 3.1 Pro]
        evidence: Criticality to core autonomous operations criterion
    resolution_status: open
    priority: high
  - id: function-level-splitting
    topic: Splitting technology IDs by function (T10a/T10b; T02 site into T15)
    positions:
      - statement: Split T10 into safety-critical (project-ending) and productivity (architecture-change) functions; fold T02 site arrays into T15
        models: [Claude Opus 5.5]
        evidence: No ground fallback for safe-abort under light time; supervised operations is a throughput fallback the economics gate can price
      - statement: Split requirements where an ID mixes essential and replaceable elements, but T10 is ruled project-ending as a whole
        models: [GPT-6.1 Sol]
        evidence: A broad label must not hide an unqualified essential function
    resolution_status: open
    priority: medium
  - id: agreed-core-source-control
    topic: Status of the 'agreed core' project-ending list
    positions:
      - statement: Treat the list as a proposed gate baseline, not evidence of unanimity, because individual classifications differ
        models: [GPT-6.1 Sol]
        evidence: For example, T02 is in the agreed core although two of three models classed it architecture-change
    resolution_status: open
    priority: medium
```