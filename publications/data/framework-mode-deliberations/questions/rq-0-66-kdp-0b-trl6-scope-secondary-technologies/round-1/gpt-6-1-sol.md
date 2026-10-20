---
questionId: "rq-0-66"
questionSlug: "kdp-0b-trl6-scope-secondary-technologies"
modelId: "gpt-6-1-sol"
modelName: "GPT-6.1 Sol"
roundNumber: 1
generated: "2026-10-17"
type: "discussion-response"
---

## 1. Frame & decision type

**Recommendation: do not impose a blanket five-technology TRL-6 requirement. Gate the capabilities on which the irreversible KDP-0B commitment depends.**

Specifically:

- **T18:** require TRL 6 for the sampling-and-assay capability supporting the selected target’s investment case, plus acceptable target-specific results.
- **T11:** accept maturity demonstrated through 0A; do not require a second demonstration simply because KDP-0B occurs later. Require TRL 6 for any unresolved scout capability whose failure could still invalidate 0B.
- **T09, T12 and T20:** require TRL 6 for the selected implementation **when 0B creates an irreversible dependence on it**. Otherwise permit TRL ≥5 only under a tightly bounded, funded substitution or deferral provision.

This is an **executive gate-policy decision**, with architecture-property consequences. The policy can be revised before commitment; expenditure and dependencies authorised at KDP-0B may not be reversible.

D-02 already resolves the governing principle: project-ending technologies need TRL 6 in a relevant environment, without waivers. The remaining issue is classification—not whether to weaken D-02.

**“Selected” is insufficient to establish criticality; “supporting” is insufficient to establish reversibility.**

## 2. Criteria and weights

First apply two **non-compensable musts**:

1. No project-ending dependency passes KDP-0B below TRL 6.
2. The target, demand, economics and licence gates remain independent; technological maturity cannot compensate for failing one.

For options satisfying those musts, use these provisional **swing weights**. They are proposed owner values, not empirical measurements.

| Criterion | Weight | Range being valued and reason |
|---|---:|---|
| **C1. Protection against irreversible exposure** | **40%** | From accepting an unresolved essential dependency to demonstrating it before commitment. This is the largest swing because it implements D-02 and protects programme viability. |
| **C2. Auditability and enforceability** | **25%** | From ambiguous labels and discretionary exceptions to testable evidence and explicit stop conditions. Gate ambiguity can defeat an otherwise sound policy. |
| **C3. Proportionate maturation cost and schedule** | **20%** | From duplicating demonstrations or maturing dispensable branches to testing only what the committed architecture needs. Important, but not exchangeable for programme survival. |
| **C4. Preservation of useful options** | **15%** | From prematurely locking implementations to retaining executable substitutions and demand-sized deployment. This supports D-01, but only within a credible delivery envelope. |

The cost criterion covers **avoidable maturation burden**, not the entire programme budget. The option-value criterion covers **usable alternatives**, not speculative redesigns.

## 3. Options

**O0 — Null: leave the panel split unresolved.**  
Argument: avoids a premature classification before architecture and mission evidence mature.  
**Reject:** teams cannot confidently define demonstrations, reserves or acceptance criteria. Deferring evidence is reasonable; deferring the rule for judging it is not.

**O1 — Blanket TRL 6 for all five at KDP-0B.**  
Argument: simple, conservative and readily auditable.  
**Reject as the general rule:** may duplicate completed 0A qualification and force maturation of implementations the programme need not irreversibly depend upon. Retain as the default where reversibility is unproven.

**O2 — Fixed categorical split.**  
Treat T11/T18 solely through their 0A mission gates; allow T09/T12/T20 at TRL ≥5 with waivers and funded maturation.  
Argument: respects mission ownership and avoids overloading KDP-0B.  
**Reject:** flight-project ownership does not remove 0B’s dependence on its evidence. Likewise, an “architecture-change” subsystem may become project-ending once a site, payload interface or power architecture is committed.

**O3 — Dependency-based gate with inherited evidence.**  
Reuse completed 0A evidence; require TRL 6 for irreversible dependencies; permit lower maturity only where an executable alternative prevents project-ending exposure.  
**Recommend:** best implements D-01 and D-02 together, albeit with a greater assurance burden.

## 4. Assessment matrix

Scores are **ordinal judgments**, from 1 = poor to 5 = strong. Weighted totals structure the discussion; they are not calculated probabilities of success.

| Option | C1: protection 40% | C2: auditability 25% | C3: burden 20% | C4: options 15% | Weighted /5 |
|---|---:|---:|---:|---:|---:|
| O0: unresolved split | 2 | 1 | 3 | 2 | **1.95** |
| O1: all five TRL 6 | 5 | 5 | 1 | 2 | **3.70** |
| O2: categorical split | 2 | 4 | 4 | 4 | **3.20** |
| O3: dependency-based | 5* | 4 | 4* | 4* | **4.40** |

\*O3 earns these scores **only with independently reviewed dependency and fallback evidence**. Without that evidence, its claimed protection and flexibility are not established; affected items revert to the TRL-6 default.

O2 also fails the mandatory screen wherever its waiver would cover a genuinely project-ending dependency. A favourable weighted score could not cure that failure.

## 5. Sensitivity vs trade-off points

### Sensitivity points — facts that can change the ruling

- **Commitment boundary:** Does KDP-0B actually authorise procurement, deployment or interface commitments that make replacement prohibitively disruptive? Moving the last responsible commitment date changes the maturity deadline.
- **Alternative feasibility:** Can the substitute meet signed Phase 1 demand within the approved economics, schedule and licence envelope?
- **Relevant environment:** Do demonstrations reproduce the dominant failure mechanisms—rather than merely resemble the operating setting?
- **Evidence inheritance:** Does 0A’s demonstrated configuration cover the capability and environment claimed at 0B?

The recommendation is most sensitive to the first two. If feasible alternatives disappear, O3 converges on O1 for the affected technology.

### Trade-off points — owner values, not facts

- How much demonstration expenditure should be accepted to avoid conditional authorisation?
- How much deployment delay is acceptable to preserve implementation flexibility?
- How much independently bounded rework risk may remain after project-ending risk has been excluded?

These require owner choices. More testing can inform them, but cannot determine the preferred balance.

## 6. Evidence certainty

The Project Dyson positions below are taken from the supplied account of `gates.md`, `gates-proposal.yaml`, `trl-baseline.yaml` and `decisions.md`; I have not independently inspected those files. GRADE labels here are adapted to engineering evidence.

| Key claim | Evidence certainty | Confidence and likelihood |
|---|---|---|
| D-02 requires TRL 6 without waivers for project-ending dependencies | **High**, as a stated decision premise | **High confidence** in the policy interpretation; likelihood is not applicable to a normative rule. |
| T18 maturity alone cannot establish economically adequate target grade | **Moderate**, based on the distinction between instrument capability and target observations | **High confidence** in the distinction. Probability of target adequacy is **unquantified**. |
| T11 evidence can be inherited without a duplicate demonstration if configuration, environment and capability remain applicable | **Moderate**, established engineering reasoning but no mission evidence supplied | **Moderate confidence** in applicability here; likelihood of a material configuration gap is **unknown**. |
| T09/T12/T20 have executable alternatives within the committed programme | **Very low**, no substitution cases supplied | **Low confidence** that any particular alternative is currently adequate; likelihood **unquantified**. |
| O3 reduces unnecessary maturation expenditure relative to O1 | **Low**, no costed work breakdown or critical path supplied | **Moderate confidence** in the mechanism, **low confidence** in the saving’s magnitude or occurrence here. |

Thus, the recommendation is **not** a finding that the three supporting systems already qualify for exceptions. It establishes what evidence would make such treatment defensible.

## 7. Key assumptions

| Assumption | Evidence that would falsify it | Consequence |
|---|---|---|
| 0A can deliver decision-quality sampling and assay evidence before 0B | Target coverage, bias, contamination or uncertainty remain insufficient for the investment case | Hold 0B, obtain additional evidence, or change target; do not substitute a TRL label for missing knowledge. |
| T11’s relevant scout functions can be completed before 0B | Continuing scouting is essential to sustain committed production or validate later irrevocable expenditure | Gate that continuing capability at TRL 6. |
| Some T09/T12/T20 choices remain reversible | Replacement requires stranded infrastructure, unqualified interfaces, unacceptable demand loss or economics-gate failure | Require TRL 6 for the selected dependency. |
| Relevant-environment demonstrations can represent dominant coupled failure modes | Analysis identifies unrepresented electrostatic/dust effects, thermal cycling, contact dynamics, transients or autonomy failures | Revise demonstration scope before awarding the gate credit. |

**ACH ranking, provisional and by least disconfirmed:**

1. **Criticality follows the committed dependency chain**, not technology identifiers. Most consistent with D-02 and the possibility of changing architectures.
2. **All five will prove effectively irreversible by 0B.** Plausible, but not established without commitment and substitution analyses.
3. **The existing categorical labels are sufficient.** Most challenged: they do not establish whether replacements preserve demand, economics and licensing.

A credible alternative case would weaken hypothesis 2. Conversely, evidence that substitution breaks the investment case would eliminate the proposed exception for that item.

## 8. Decision, warrant, accepted downside

### Proposed rule text

> **At KDP-0B, every technology capability whose failure would invalidate the authorised investment case shall have demonstrated TRL 6 in a documented relevant environment. No maturity waiver is permitted for such a capability.**
>
> **Previously accepted 0A evidence may satisfy this requirement where its configuration, operating envelope and demonstrated functions remain applicable. Completion of a mission, or assignment of a technology-level TRL, does not by itself establish applicability.**
>
> **For T09, T12 and T20, the selected reference implementation is the configuration used in the approved architecture, performance model, cost estimate, interfaces and qualification plan—not merely a preferred candidate. It requires TRL 6 where KDP-0B creates an irreversible dependence upon it.**
>
> **An implementation at TRL ≥5 may be accepted only if independent review verifies a funded, scheduled and interface-compatible alternative or deferral that preserves the approved demand, economics, safety and licence case. The alternative must itself be sufficiently demonstrated for its assigned role.**
>
> **Each exception shall identify its owner, evidence, contingency funding, latest substitution date and automatic stop trigger. No irreversible commitment dependent on that implementation may occur after that date without TRL 6 or activation of the accepted alternative.**

### Technology-specific application

- **T18:** require TRL 6 for the relevant sampling and assay capability **and** target-specific evidence meeting predeclared uncertainty and representativeness criteria.
- **T11:** inherit satisfactory 0A demonstration evidence. Gate outstanding critical functions, not the spacecraft’s historical existence.
- **T09:** assess distribution, insulation, protection and load interaction under the selected site conditions.
- **T12:** require evidence addressing the selected 150–300 t payload regime and governing contact/control dynamics; a small demonstration needs a validated scaling argument.
- **T20:** assess storage together with the microgrid functions on which operations depend, including transient response, fault isolation and degraded operation.

**Warrant:** D-02 ties stringency to irreversibility. Evidence inheritance avoids duplicate work; demonstrated substitutability distinguishes a reversible implementation risk from a project-ending dependency.

**Accepted downside:** this policy requires more assurance work and judgment than a blanket list. It may still conclude that all five need TRL 6.

## 9. Consequences

Before KDP-0A, adopt the classification procedure and assign evidence owners. Before KDP-0B, require an independently reviewed dependency map and, for every proposed exception, a costed substitution case and commitment schedule.

This decision:

- **Enables** reuse of 0A evidence and demand-sized 0B planning under D-01.
- **Constrains** procurement and interface commitments that would silently make a lower-maturity implementation indispensable.
- **Does not relax** the target, demand, economics or licence gates.
- **Preserves** the pre-committed “0A only, Earth supply” outcome if required evidence is unavailable.

**Y-statement:** In the context of D-01’s gated real option and D-02’s no-waiver rule, facing disputed technology labels and potentially irreversible dependencies, we choose capability-based TRL-6 gating with inherited 0A evidence and strictly demonstrated reversibility, to protect the investment case without unnecessary duplicate maturation, accepting additional assurance effort. **The warrant is that irreversibility—not list membership—determines required stringency; the qualifier is that any unproven substitution defaults to TRL 6, constraining 0B authorisation until the dependency is demonstrated or removed.**