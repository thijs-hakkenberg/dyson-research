---
questionId: "rq-0-73"
questionSlug: "scout-trl-milestone"
type: "discussion-conclusion"
generatedBy: "claude-opus-5-5"
generated: "2026-10-17"
framework: "18f503fe4ec6"
roundCount: 1
terminationReason: "unanimous-conclude"
role: "alternate synthesis"
---

# Scout and Sampling-Payload TRL Milestones (rq-0-73): Round 1 Synthesis

## Summary

After one round the panel agreed on part of the ruling.
- **Shared ground.** All three models reject the null option of leaving the split as it is. All three set **TRL 6 at scout PDR** for T11 (rendezvous scout) and T18 (subsurface sampling and assay). All three say the target gate cannot pass before in-situ sampling data has come back from the target.
- **Restating the split.** Each model, separately, re-read the earlier disagreement as mostly a difference in *milestone* rather than in *level*.
  - Claude ranked H1 (milestone/vocabulary) least disconfirmed.
  - GPT ranked "different milestones and objects of assessment" least disconfirmed.
  - Gemini built its synthesis on the same separation.

**Claude and GPT** go further, to near-identical layered rules:
- TRL 6 at PDR;
- the actual flight system, including the sampling payload, flight-qualified before launch, which both label TRL 8;
- a target gate keyed to a predeclared sampled-data specification rather than a TRL label.

**Gemini** diverges on two points:
- It holds, with "High" certainty, that TRL 8 cannot be reached before first flight, so it sets no pre-launch TRL 8 criterion.
- It keys the target gate to T18 reaching TRL 7 through in-situ demonstration.

Claude's and GPT's votes both rejected Gemini's response, citing that TRL 8 premise as the weakest link (information).

Two disagreements remain open.

1. **A factual or definitional one: does strict NASA TRL 8 presuppose prior operational flight for a first-of-kind system?**
   - Gemini says yes.
   - GPT says no, citing NASA/SP-2016-6105.
   - Claude's response says strict NASA wording creates that problem for first-of-kind T18. It proposes declaring ISO 16290 as the scale to dissolve it. Claude's own vote, however, states that both the NASA and ISO definitions treat TRL 8 as flight qualification through ground test. GPT's vote marked Claude's NASA–ISO incompatibility claim as "not established".
2. **What KDP-0B requires of T18.**
   - Claude: T18 must be demonstrated in flight, otherwise the fallback "0A only, Earth supply" applies.
   - Gemini: KDP-0B is not triggered until T18 reaches TRL 7 in situ.
   - GPT: retain D-02's TRL 6 in a relevant environment, without waiver.

## Decision record

The panel converged only partly. The converged core is set out first, then one Y-statement per remaining position.

**Converged core (all three models)**
- Reject the null option.
- Set TRL 6 at scout PDR for T11 and T18. The relevant environment is a defined ground or analogue envelope.
- Schedule the target gate after in-situ sampling data has been returned.

**Position 1: laddered rule on a declared ISO 16290 scale (Claude Opus 5.5)**
- **Context and problem.** *In the context of* the 0A scouts being the first flight hardware and the only source of sampled-grade evidence, *facing* a panel split that is mostly about milestones and scale wording, and a T18 whose decisive behaviour only space can reveal,
- **Choice.** *we chose* a declared ISO 16290 ladder:
  - TRL 5 at SRR;
  - TRL 6 at PDR;
  - flight-qualified (ISO TRL 8) at scout-1 launch release, with acceptance testing for later scouts;
  - a data-specification target gate;
  - T18 demonstrated in flight at KDP-0B, otherwise the fallback.
- **Aim.** *to achieve* stringency that tracks reversibility, a launch-release criterion that prevents avoidable losses, and a target gate that discriminates on what it actually needs,
- **Accepted cost.** *accepting* roughly a 30–40% chance (Claude's judgement, low confidence) that scout #1 fails in situ, which would delay the target gate and possibly trigger Earth supply.
- **Warrant:** each gate's criterion should test the decision that gate makes: design commitment, spending a unit, target worth, and one-way commitment respectively.
- **Qualifier:** "presumably right, if A1 (two or more scouts, launches staggered by six months or more) and A2 (a credible T18 analogue environment by about month 9) hold."
- **Accepted downside:** failure of scout #1 and slip of the target gate.

**Position 2: layered rule on the programme's adopted TRL definition (GPT-6.1 Sol)**
- **Context and problem.** *In the context of* D-01's gated 0B option and D-02's reversibility-based assurance policy, *facing* conflicting scout TRL requirements attached to different milestones,
- **Choice.** *we chose*:
  - TRL 6 for critical novel technologies at PDR;
  - TRL 8 (flight-qualified) for each actual flight system before launch, proportionate to mission class;
  - validated sampling evidence against predeclared thresholds for the target gate;
  - D-02's TRL 6 for project-ending technologies at KDP-0B.
- **Aim.** *to achieve* credible flight readiness and an evidence-based resource decision,
- **Accepted cost.** *accepting* more early qualification effort, a possibly later PDR, and the possibility that a technically successful scout still fails the target gate.
- **Warrant:** technology demonstration, flight qualification and investment evidence answer different failure questions. Requiring all three prevents substitution between them.
- **Qualifier:** PDR timing can be revised on a documented test-and-cost case. Launch qualification and target evidence cannot.
- **Accepted downside:** as above. GPT calls a failed target gate after a working scout "an intended outcome of honest discrimination".

**Position 3: TRL 6 at PDR, TRL 7 at target gate (Gemini 3.1 Pro)**
- **Context and problem.** *In the context of* Phase 0A target validation, *facing* a panel split on scout readiness levels,
- **Choice.** *we chose* TRL 6 at PDR, with the target gate and KDP-0B blocked until T18 achieves TRL 7 through in-situ demonstration,
- **Aim.** *to achieve* strict adherence to aerospace standards and rigorous evidence for KDP-0B,
- **Accepted cost.** *accepting* that the first scout launch acts as a TRL 7 technology demonstration rather than a mature operational asset.
- **Warrant:** a system cannot reach TRL 7 or 8 without spaceflight, so the mission itself bridges TRL 6 to TRL 7. Both other models contest this premise.
- **Qualifier:** not stated explicitly. Assumption 2 notes that a single-scout 0A would require heavier ground qualification.
- **Accepted downside:** risk of in-flight failure.

## Decision-quality audit

| Response (Round 1) | Weakest DQ link named in votes | Scaffold steps missing or unsupported | Trade-off (values) points vs facts |
|---|---|---|---|
| **Claude Opus 5.5** | Reasoning (self, APPROVE); alternatives (Gemini, APPROVE); information (GPT, NEUTRAL) | **Step 6:** GPT judged the claimed NASA–ISO incompatibility on TRL 8 "not established". That claim shapes the scale choice, and Claude's own vote on Gemini states the opposite reading of NASA. **Step 4:** the O4 margin over O1 is thin and, by Claude's own account, sensitive to C3. Claude says dropping C3 to 5 "roughly ties" them. Recomputed from Claude's matrix, O1 scores 3.95, not the reported 4.00; the ranking is unchanged. **Step 3:** Gemini noted that options were rejected in the text before the matrix. | **Values:** T1, first-scout risk vs time to target gate, which Claude calls an owner risk-appetite call. T2, label vs data at the target gate, explicitly called "a legitimate values difference". **Facts:** S1 (scale definition), S2 (fleet size), S3 (fidelity of a T18 analogue). |
| **Gemini 3.1 Pro** | Information (Claude, REJECT; GPT, REJECT); alternatives (self, NEUTRAL) | **Step 6:** "High" certainty that TRL 8 is unreachable before first flight. Claude and GPT both call this incorrect or uncalibrated, and the rejection of GPT's position rests on it. **Step 4:** the matrix is qualitative only, with no scores. **Step 3:** no precursor option, and options were rejected before assessment. **Step 7:** no ACH. **Step 8:** no launch-release criterion, and the target gate is keyed to a TRL label (Claude, GPT). Gemini frames the decision as one-way overall, which differs from Claude's per-milestone reversibility analysis. | **Values:** schedule velocity vs in-flight failure risk. **Fact (disputed):** whether TRL 8 requires prior flight. This is definitional and checkable, not a values question. |
| **GPT-6.1 Sol** | Alternatives (Claude, APPROVE; Gemini, APPROVE); commitment (self, APPROVE) | **Step 3:** no precursor-flight option and no single-scout variant as distinct options. Claude says B and C are "partly straw men", so the 4.60 vs 2.75 margin overstates D. GPT itself says the margin is not the main basis. **Step 8:** test envelopes and evidence thresholds are deferred to implementation, as GPT acknowledges. Claude described leaving T18 at TRL 6 for KDP-0B as compliant with D-02 but weaker. | **Values:** PDR maturity vs design flexibility; qualification spend vs tolerated scout loss; more reconnaissance vs delayed 0B. **Facts:** fidelity of the relevant environment, qualification inheritance, evidence latency, sampling representativeness. |

## Key Points

**Where all three agree**
- **Null option rejected.** Leaving the split would leave PDR, launch and target-gate criteria undefined or conflated (all three).
- **TRL 6 at scout PDR** for T11 and T18 (all three). GPT adds that the exact PDR placement is the least robust element, and that a controlled TRL-5-at-PDR path could change it.
- **Target-gate timing.** The gate cannot come before the scout has sampled and assayed the target (all three).
  - GPT adds that the data must also be validated and independently reviewed.
  - Claude estimates the earliest target gate at roughly month 36–66 (judgement, medium confidence on the range, low on the point value).
- **Fleet size changes the rigour required.** A single-scout 0A would justify stricter pre-launch ground qualification (Claude S2/A1; Gemini Assumption 2).

**Where Claude and GPT agree (Gemini differs)**
- **Launch release needs explicit flight qualification** of the integrated spacecraft and payload.
- **The target gate should be keyed to a predeclared sampled-data specification, not a TRL label.**
  - Claude: sample count, depth, assay uncertainty derived from g-economics, spatial coverage.
  - GPT adds contamination/calibration, geological representativeness, relevance to extraction, and thresholds set before flight.

**Positions held by one model only**
- **Claude**
  - TRL 5 at scout SRR.
  - ISO 16290 / ECSS-E-HB-11A as the declared scale, with a NASA crosswalk.
  - Qualify once (protoflight or qualification model), then acceptance test later units.
  - Precursor pathfinder (O5) rejected at an estimated +18–36 months and $50–150M (not costed), because "the scouts are the pathfinder".
- **GPT**
  - Non-compensable requirements (D-02, safety and licensing, no target pass without adequate evidence) that a weighted score cannot override.
  - An evidence register linking each maturity claim to its configuration and environment.
  - A working sampler can return a precise measurement of an unrepresentative location (sampling representativeness).

## Unresolved Questions

1. **TRL 8 definition.** Does NASA TRL 8 (NPR 7123.1 / SP-2016-6105) require prior operational flight for a first-of-kind system? Gemini says yes. GPT says no. Claude's response and Claude's vote take different stances. This is the hinge of the launch-release dispute.
2. **Which TRL scale is declared.** Claude proposes ISO 16290. GPT proposes "the programme's adopted definition" and cites NASA. Gemini uses NASA/DoD.
3. **What KDP-0B requires of T18.** The options are flight-demonstrated in situ (Claude) or TRL 7 in situ (Gemini), versus D-02's TRL 6 in a relevant environment (GPT). The panel did not address whether GPT's target-gate requirement for in-situ results makes this difference practically moot.
4. **Later-scout launches.** Does "TRL 8 before each launch" (GPT) mean full requalification, or acceptance against the qualified design (Claude)? GPT's "proportionate to mission class" wording may be compatible, but this was not confirmed.
5. **Fleet size and launch stagger.** Claude's ruling rests on two or more scouts with staggered launches. GPT did not model a single-scout variant.
6. **T18 relevant environment.** Can a credible reduced-gravity regolith analogue be defined, by about month 9 (Claude A2)? If not, Claude, GPT and Gemini all indicate PDR must be re-planned, not waived. GPT and Claude mention a precursor as a possible fallback.
7. **Owner risk appetite for scout #1** (Claude T1; GPT's qualification-spend vs loss trade-off).
8. **Can g-economics state a required grade uncertainty** so the data specification can be written (Claude A4)?

## Recommended Actions

1. **Settle the TRL 8 definitional question from source text** before adopting rule wording. Check NPR 7123.1, NASA/SP-2016-6105 Rev 2 and ISO 16290 TRL 7–8 definitions, then record the crosswalk in `trl-baseline.yaml`. (Raised by Claude S1 and by the GPT and Claude votes.)
2. **Owner to declare the TRL scale** for all gates in `gates-proposal.yaml` (Claude; GPT's "adopted definition").
3. **Adopt the converged core now:** null rejected, TRL 6 at PDR, target gate after returned in-situ data. Decide separately on:
   - the launch-release criterion (Claude/GPT flight qualification vs Gemini no pre-launch TRL 8);
   - the target-gate key (data specification, Claude/GPT, vs TRL 7, Gemini).
4. **Owner ruling on T18 at KDP-0B** (Claude/Gemini in-situ demonstration vs GPT D-02 TRL 6), recorded against the pre-committed fallback "0A only, Earth supply".
5. **Fix the scout fleet size and launch stagger**, or record them as an explicit assumption. Claude treats both as load-bearing.
6. **Fund a T18 test-facility survey and relevant-environment envelope for months 0–12** (Claude; GPT's test-gap assessment).
7. **Write the g-target sampled-data specification jointly with g-economics before flight** (Claude; GPT "not negotiated after seeing favourable samples").
8. **Record in `decisions.md` that the target gate and KDP-0B are event-driven, not calendar-fixed**, so slips are not read as failures (Claude; GPT treats month 12–24 as a planning window).
9. **Elicit the owner's risk appetite for scout #1** to settle the precursor (O5) question (Claude T1).

```yaml
questionId: "rq-0-73"
topics:
  - id: trl-8-prior-flight-definition
    topic: Whether TRL 8 can be reached before first flight
    positions:
      - statement: TRL 8 (flight-qualified through test and demonstration) does not require a prior operational mission and is a legitimate pre-launch criterion
        models: [GPT-6.1 Sol]
        evidence: NASA/SP-2016-6105 Rev 2 TRL descriptions; flight qualification distinct from mission operation
      - statement: Under ISO 16290 TRL 7-8 are ground-achievable, but strict NASA wording makes pre-launch TRL 8 incoherent for first-of-kind T18; declaring ISO dissolves the conflict (Claude's vote separately states both NASA and ISO treat TRL 8 as ground-test qualification)
        models: [Claude Opus 5.5]
        evidence: NPR 7123.1 TRL 7 operational-environment wording; ISO 16290 'accepted for flight'
      - statement: TRL 8 cannot be achieved before first launch of a novel system
        models: [Gemini 3.1 Pro]
        evidence: Standard NASA/DoD definitions, asserted at High certainty
    resolution_status: open
    priority: critical
  - id: launch-release-criterion
    topic: Readiness criterion at scout launch release
    positions:
      - statement: Scout 1 flight-qualified (ISO TRL 8 via qualification or protoflight); later scouts acceptance-tested to qualified design plus anomaly closure
        models: [Claude Opus 5.5]
        evidence: Environmental-test escapes as classic cause of small-spacecraft first-unit loss; D-02 proportionality with multi-scout fleet
      - statement: Each scout's actual integrated spacecraft and payload flight-qualified at TRL 8, proportionate to mission class, plus mission-assurance closures
        models: [GPT-6.1 Sol]
        evidence: TRL 6 alone does not establish launch readiness; distinct assurance claims
      - statement: No pre-launch TRL 8 requirement; first launch acts as TRL 7 technology demonstration
        models: [Gemini 3.1 Pro]
        evidence: Premise that TRL 8 requires spaceflight
    resolution_status: partially-resolved
    priority: high
  - id: target-gate-criterion
    topic: Pass criterion for the target gate
    positions:
      - statement: Key to a predeclared sampled-data specification; TRL 7 recorded as a consequence, not a criterion
        models: [Claude Opus 5.5, GPT-6.1 Sol]
        evidence: A scout can reach TRL 7 yet return non-decision-grade data; sampling representativeness can dominate instrument performance
      - statement: Target gate passes only when T18 achieves TRL 7 via in-situ operational demonstration
        models: [Gemini 3.1 Pro]
        evidence: Ties gate to demonstrated in-space function
    resolution_status: partially-resolved
    priority: high
  - id: kdp-0b-t18-requirement
    topic: T18 maturity required at KDP-0B
    positions:
      - statement: T18 demonstrated in the operational environment (in-situ sampling and assay on at least one target), no waiver; otherwise fallback or deferral
        models: [Claude Opus 5.5]
        evidence: T18 project-ending; D-02 no waiver at one-way gate; ground cannot reproduce low-g regolith interaction
      - statement: KDP-0B not triggered until T18 reaches TRL 7 in situ
        models: [Gemini 3.1 Pro]
        evidence: Operational demonstration needed for rigorous KDP-0B evidence
      - statement: All project-ending technologies meet D-02 TRL 6 in relevant environment, no waiver; scout success confers no maturity on extraction technologies
        models: [GPT-6.1 Sol]
        evidence: D-02 as accepted
    resolution_status: open
    priority: critical
  - id: trl-scale-declaration
    topic: Which TRL scale governs the gates
    positions:
      - statement: Declare ISO 16290 / ECSS-E-HB-11A with NASA crosswalk
        models: [Claude Opus 5.5]
        evidence: Scale ambiguity is a disguised waiver under D-02
      - statement: Use the programme's adopted definition, citing NASA SP-2016-6105
        models: [GPT-6.1 Sol]
        evidence: NASA TRL descriptions
      - statement: Strict NASA/DoD definitions
        models: [Gemini 3.1 Pro]
        evidence: Avoid semantic drift
    resolution_status: open
    priority: high
  - id: pdr-trl-level
    topic: TRL required at scout PDR
    positions:
      - statement: TRL 6 in a documented relevant environment for T11 and T18 at PDR
        models: [Claude Opus 5.5, Gemini 3.1 Pro, GPT-6.1 Sol]
        evidence: NASA practice of TRL 6 by PDR; GPT notes PDR placement is least robust element and TRL 5 path could be justified
    resolution_status: resolved
    priority: medium
  - id: fleet-size-dependence
    topic: Dependence of the ruling on number of scouts
    positions:
      - statement: Ruling assumes two or more scouts with launches staggered by six months or more; a single scout requires a stricter pre-launch T18 campaign
        models: [Claude Opus 5.5, Gemini 3.1 Pro]
        evidence: Launch is two-way at programme level only with multiple units
      - statement: Not modelled as a separate variant; required sequence depends on predeclared evidence sufficiency plan
        models: [GPT-6.1 Sol]
        evidence: Do not require every scout to launch before target gate
    resolution_status: open
    priority: high
  - id: precursor-demo
    topic: Whether a precursor T18 flight demo is needed
    positions:
      - statement: Rejected; scouts are the pathfinder; adds 18-36 months and an estimated $50-150M (not costed); competitive only if no ground analogue exists and a cheap rideshare does
        models: [Claude Opus 5.5]
        evidence: Demo environment still not target regolith
      - statement: May be necessary if ground testing cannot reproduce coupled low-g effects
        models: [GPT-6.1 Sol]
        evidence: Relevant-environment fidelity sensitivity point
    resolution_status: open
    priority: medium
  - id: srr-trl-level
    topic: TRL at scout SRR
    positions:
      - statement: TRL 5 at SRR with the T18 relevant-environment envelope defined
        models: [Claude Opus 5.5]
        evidence: D-02 TRL 4-5 for two-way 0A milestones
    resolution_status: open
    priority: low
```