---
questionId: "rq-0-64"
questionSlug: "t26-comms-trl-rating-object"
modelId: "claude-opus-5-5"
modelName: "Claude Opus 5.5"
roundNumber: 1
generated: "2026-10-17"
type: "discussion-response"
---

# T26 Rating Object: Rate the Integrated Authenticated Service, with Its Parts Shown Underneath

## 1. Frame and decision type

**The decision.** Which object does T26 rate: heritage components, a composite with integration credit, or the integrated service? How is that object reported and gated? The answer sets the rule for the other composite technologies in the WP-A re-baseline.

**Decision type.** This is a *property decision* in Kruchten's terms: it sets a rule that constrains every later rating and gate. It is not a one-off executive call about T26 alone.

**Reversibility.** The decision is cheap to reverse on paper. It is expensive to reverse in practice. If T26 drops off the KDP-0B list now, no funded path to TRL 6 gets planned in Phase 0A. Finding the gap at KDP-0B would then cost the remaining Phase 0A schedule.

**Cynefin domain.** The question is *complicated*, not complex. The facts are mostly agreed. The panel split on what was being rated, not on what is known. That calls for an explicit rule, not more elicitation.

**What is known, what can be done, what is wanted:**
- **Known:** RF links are mature. DTN has been demonstrated in deep space. Conjunction operations are routine. Authenticated fleet command with key lifecycle across outages has no cited deep-space record. Data rates are undefined.
- **Can do:** choose the rating object, the reporting format, the risk class and the gate criterion.
- **Want:** a gate that asks for the evidence that actually bounds Phase 0B risk, applied the same way across all 26 technologies.

## 2. Criteria and swing weights (stated before options)

| # | Criterion | Swing range considered | Weight | Why this weight fits the range |
|---|---|---|---|---|
| C1 | **Fidelity to the TRL brief rule**: rate at the scale, environment and duration the architecture requires | From "rates something the architecture doesn't use" to "rates exactly the required configuration" | **0.30** | Widest swing. It is the governing rule of the brief, and it alone moves T26 by 3–4 TRL levels. |
| C2 | **Gate usefulness**: does KDP-0B end up demanding the evidence that bounds Phase 0B risk? | From "gate silent on the weakest element" to "gate names and tests it" | **0.25** | Large swing. A wrong object either removes T26 from the gate or gates on the wrong test. |
| C3 | **Diagnostic information preserved**: can a reader see where maturity is and isn't? | From one opaque number to a full decomposition | **0.15** | Moderate swing. Information loss is recoverable if the working files survive, but the published baseline is what gets read. |
| C4 | **Consistency and portability** across the other composite technologies | From "T26-specific fudge" to "general rule applicable to all 26" | **0.15** | Moderate. Only a handful of the 26 are strongly composite, but inconsistency undermines the whole re-baseline. |
| C5 | **Avoiding false alarm**: not inflating risk or cost where heritage really is mature | From "flags mature RF as immature" to "credits heritage correctly" | **0.10** | Real but narrow swing. Everyone agrees the RF links are TRL 9, so any sensible option can show that. |
| C6 | **Communicability and process cost** | From "needs a page of caveats" to "one line" | **0.05** | Smallest swing. The gap between one number and one number plus a short table is small. |

**Must-criteria (Kepner-Tregoe screen), applied before scoring:**
- **M1.** The option must not rest on uncited claims. Per the brief: "cite or say unsure."
- **M2.** The option must state the configuration being rated, in line with NASA NPR 7123.1 TRL definitions.

## 3. Options

**O0. Null option.** Publish the three panel ratings as a 3–7 range with the synthesis note.
- Rejected. It fails M2: there is no stated configuration.
- It hands the gate designer an unresolved disagreement and lets the most optimistic reading win by default.

**O1. Heritage components (Gemini's object).** Headline TRL 6–7.
- Rejected. It fails M1. The pivotal "SDLS has flown on multiple missions" claim names no mission. I am not aware of a published deep-space record of CCSDS SDLS (CCSDS 355.0-B) authenticated commanding with on-orbit key management and post-outage key recovery. I am *unsure* whether such a record exists, and that uncertainty is itself the point.
- It also fails C1: it rates a configuration the architecture does not fly.

**O2. Composite with integration credit (Claude's object).** Headline 5–7.
- Defensible practice, but the range is too wide to gate on.
- Claude's own caveat concedes the upper bound ignores a 2–4× node-count gap and the authentication gap.
- Rejected as the headline object. Its evidence base is retained in the sub-ratings.

**O3. Integrated service only (GPT's object).** Headline TRL 3, with 4 conditional, and no sub-ratings published.
- Correct object, but it discards real information (C3, C5).
- It invites the reading "deep-space comms is TRL 3", which is false for the links and will be contested by anyone with DSN experience.

**O4. Integrated service as the headline, plus a mandatory sub-rating table and a weakest-link rule.** Recommended. The rule has three parts:
1. **Headline** is the TRL of the integrated service in the required configuration (≥29 nodes, store-and-forward through the longest outage, authenticated command with key lifecycle, no Earth-dependent safety action).
2. **Cap:** the headline can never exceed the lowest *critical* sub-rating. It can never exceed the integration TRL either, unless an integrated article has been tested.
3. **Sub-ratings** are published with the headline, each with its own configuration, evidence citation and uncertainty. They are never averaged.

**O5. Split T26 into separate technologies.**
- The split: T26a (deep-space RF and DTN relay, TRL 6–7) and T26b (authenticated fleet command and key management, TRL 3–4), with integration handled as a system-level gate item.
- This is the strongest rival. It isolates the weak element cleanly.
- I reject it narrowly. Fleet scale and outage recovery fall *between* T26a and T26b. Neither child owns "29 nodes through a solar-exclusion outage with keys still valid afterwards." That interface is exactly where the panel says the gap lives.

## 4. Assessment matrix (QOC)

Scores run from 1 (poor) to 5 (best). O0 and O1 fail the must-screen; their scores are shown only for completeness.

| Criterion (weight) | O0 Null | O1 Heritage | O2 Composite | O3 Integrated only | **O4 Integrated + subs** | O5 Split |
|---|---|---|---|---|---|---|
| M1 cited / M2 configuration stated | ✗ / ✗ | ✗ / ✓ | ✓ / partial | ✓ / ✓ | ✓ / ✓ | ✓ / ✓ |
| C1 Fidelity (0.30) | 2 | 1 | 3 | 5 | 5 | 4 |
| C2 Gate usefulness (0.25) | 1 | 1 | 2 | 4 | 5 | 4 |
| C3 Diagnostic info (0.15) | 3 | 2 | 3 | 1 | 5 | 4 |
| C4 Consistency (0.15) | 1 | 3 | 3 | 4 | 5 | 3 |
| C5 No false alarm (0.10) | 3 | 5 | 4 | 2 | 4 | 5 |
| C6 Communicability (0.05) | 2 | 5 | 3 | 4 | 3 | 3 |
| **Weighted total** | 1.85 | 1.90 | 2.90 | 3.75 | **4.80** | 3.90 |

**Robustness check.** O4 still leads if C1 drops to 0.15 and C5 rises to 0.25: O4 ≈ 4.5 versus O5 ≈ 4.2. O5 overtakes only if C4 is weighted near zero *and* someone is assigned to own the integration interface. If that ownership is explicit, the remaining gap between O4 and O5 is mostly presentation.

## 5. Sensitivity points and trade-off points

### Sensitivity points (facts that move one attribute strongly)

**S1. A cited deep-space SDLS-or-equivalent flight record with key management.**
- If it exists, the authentication sub-rating moves from 3–4 toward 6–7.
- It would *not* lift the headline above the integration TRL, because no integrated article exists. The headline moves from 3 to about 4, not to 6.
- This is the single most valuable piece of evidence to chase.

**S2. Outage durations for the actual orbits.**
- Mars superior conjunction gives roughly two weeks of command moratorium. That has been routine since at least the MER era.
- The SEL1 node is the sensitive case. A Sun–Earth L1 asset sits near the Sun line as seen from Earth by definition. Halo and Lissajous orbits are usually chosen with amplitudes that keep them outside the solar-exclusion cone, and some Lissajous geometries pass through it periodically.
- Whether the SEL1 node sees repeated exclusion sets the key-validity window, the bundle storage depth and the autonomy duration requirement. It can change the authentication design: for example, key lifetimes have to outlast the longest outage, with pre-positioned rekey material.

**S3. Traffic budget.**
- With no data rates defined, "relevant environment" cannot be bounded quantitatively.
- A tight budget makes MSPA-style shared-aperture scheduling credible. A large budget (e.g. site-plant telemetry or imaging) could force dedicated relay assets. That is an architecture change, which supports the risk class below.

**S4. Node count.** The range 15–29 matters. At 15, the Mars Relay Network plus DSN analogy is roughly 2× short. At 29, it is 4× or more.

### Trade-off points (values questions, not facts)

**T1. Conservatism versus schedule and cost.**
- Gating on the integrated service at TRL 6 forces a funded demonstration in Phase 0A, estimated at 3–5 years (GPT) or 2–4 years (Claude).
- Accepting heritage credit saves that cost but carries the gap into 0B. This is a risk-appetite choice for the owner, not something analysis settles.

**T2. Is command security safety-critical or mission-assurance?**
- If D-03 makes command security a licence condition for high-energy tug operations, losing trustworthy command stops those operations. That makes it a candidate for project-ending.
- If it stays a mission-assurance matter, it is architecture-change. This is a policy and values judgment, partly external to the project.

**T3. Headline simplicity versus honesty of decomposition.**
- One number reads cleanly. A number plus a table is more honest.
- O4 deliberately pays a small communicability cost (C6) to protect C3.

## 6. Evidence certainty

Likelihood (how probable the claim is) is kept separate from confidence (how good the evidence is), following IPCC and ICD 203 practice.

| Claim | Evidence | GRADE certainty | Likelihood / confidence |
|---|---|---|---|
| Interplanetary RF links via DSN are mature | Decades of DSN operations; MSPA used operationally for Mars assets | High | Virtually certain / high |
| DTN demonstrated in deep space | DINET on EPOXI (2008); later DTN operations on ISS | Moderate. The demonstration was small-scale, short-duration and few nodes. | Very likely mature as a protocol; low confidence at 29-node, multi-month store scale |
| Conjunction operations are routine | Mars missions through every conjunction since the 2000s | High for Mars-class geometry | Virtually certain; *not* transferable to SEL1 without orbit-specific analysis |
| Multi-asset relay at fleet scale | Mars Relay Network (MRO, Odyssey, MAVEN, TGO) serving several landers | Moderate as an analogue; low as a prototype of the required configuration | Likely extensible; medium confidence; node gap 2–4× |
| SDLS authenticated commanding with key lifecycle in deep space | CCSDS 355.0-B standard exists; **no flight record cited by any panellist** | Very low | Unknown; I am unsure a qualifying deep-space record exists |
| Post-outage key recovery demonstrated | None cited | Very low | Unlikely to have been demonstrated in the required form; low confidence either way |
| Integrated service at required scale has precedent | Panel agreement that none exists | Moderate. This is a negative claim, but all three models agree and none could name one. | Very likely no precedent |

Multi-model agreement is recorded as *agreement*, not as evidence, per the brief.

## 7. Key assumptions and what would falsify them

| # | Assumption | Falsified by |
|---|---|---|
| A1 | The authentication and key-lifecycle element is the binding constraint | A cited deep-space SDLS (or equivalent) record with on-orbit rekeying, *or* a design showing keys need no on-orbit lifecycle within mission duration (pre-loaded long-life keys accepted by the licensing authority) |
| A2 | Integration at fleet scale is non-trivial, so it is not an extrapolation of the Mars Relay Network | A credible scheduling and traffic analysis showing ≥29 nodes fit within existing DSN aperture and relay capacity at the defined data rates, with margin |
| A3 | Ground testbeds with real DSN passes plus emulated light time and outages can count as "relevant environment" for TRL 6 | A stricter project ruling that TRL 6 needs a space segment, which would push the timeline toward the 3–5 year upper end and require a hosted payload or pathfinder |
| A4 | Failure leads to architecture change (more relays, fewer concurrent assets, restricted tug autonomy), not project end | A D-03 licence condition that makes demonstrated command security a precondition for tug operations, with no degraded-mode alternative |
| A5 | Phase 0A is long enough to fund a path to TRL 6 | A Phase 0A duration under about 3 years, which makes T26 schedule-critical and argues for starting the testbed immediately |

### Competing hypotheses for the panel divergence (ACH)

| Hypothesis | Disconfirming evidence | Rank |
|---|---|---|
| **H1. The panellists rated different objects** | Barely any. All three agree on the facts, and GPT's sub-ratings (RF 9, DTN 7, conjunction 9, auth 3–4) reproduce Claude's and Gemini's component views. | **1st, least disconfirmed** |
| **H3. They read "relevant environment" differently** | Partly consistent: Gemini treats "relevant space environments" for the protocols as sufficient. This is a sub-case of H1. | 2nd |
| **H2. They disagree on facts** (the SDLS flight record) | Real but narrow. Only Gemini asserts the record, and uncited. Removing that claim leaves Gemini's rating at about 5–6, not 3. Facts alone do not explain the whole spread. | 3rd |

The synthesis finding stands. Fix the object first. Then resolve H2 by citation, not by deliberation.

## 8. Decision, warrant, accepted downside

### Decision

**Rating object and reporting.** T26 is rated as the **integrated, authenticated deep-space command and communications service in the configuration the architecture requires.** That configuration is:
- 15–29 concurrent assets;
- store-and-forward through the longest orbit-specific conjunction or exclusion outage;
- 1–25 minute light time;
- authenticated command with key lifecycle, including post-outage recovery;
- no safety-critical action dependent on an Earth response.

The headline is reported with a mandatory sub-rating table. The headline is capped by the lowest critical sub-rating and by the integration TRL. Sub-ratings are never averaged.

**Ratings to carry into the baseline:**

| Element | TRL | Basis |
|---|---|---|
| **Headline: integrated service** | **3 (4 conditional on a configuration-controlled integrated breadboard)** | No integrated article; capped by the authentication sub-rating |
| RF links | 9 | DSN heritage |
| DTN store-and-forward | 6–7 | DINET flight; limited scale |
| Conjunction operations | 9 for Mars-class; TBD for SEL1 | SEL1 pending exclusion analysis |
| Multi-asset relay scheduling | 5–6 | Mars Relay Network and MSPA; node gap |
| Authenticated fleet command and key lifecycle | 3–4 | No cited deep-space record |

**Risk class.** *Architecture-change*, with a **standing flag to escalate to project-ending if D-03 makes command security a licence condition.**

Given that conditional, I recommend applying the D-02 TRL 6 requirement to T26 at KDP-0B now, rather than waiting for D-03 to resolve. Waiting is the expensive error.

**KDP-0B criterion.** T26 passes only if all of the following hold:
1. **Defined inputs exist.** A defined traffic budget and orbit-specific outage durations, including SEL1, are configuration-controlled. This is an entry condition: no test is valid without them.
2. **Integrated TRL 6 demonstration.** It must include:
   - representative flight-like radios and command processors for at least a subset of nodes, with the rest emulated, totalling ≥29 nodes;
   - real DSN passes with at least one deep-space-distance link;
   - injected outages at the maximum required duration;
   - SDLS-class authentication with rekey and post-outage key recovery;
   - red-team command-injection and replay attempts;
   - local safe actions taken without Earth response, verified against predictions.
3. **Independent assurance case.** An assurance case (GSN) for command integrity is reviewed independently, and the licensing authority's view is recorded if D-03 is active.

**Rule for other composites.** Every composite technology in the re-baseline is rated as the integrated article at required configuration, with a published sub-rating table and the same weakest-link cap. Where a composite has no integrated article, the headline cannot exceed TRL 4.

### Y-statement

*In the context of* the Phase 0 TRL re-baseline, where T26 is a composite service whose parts range from TRL 9 to TRL 3–4,
*facing* a panel split caused by rating different objects, an uncited authentication claim, and a gate rule (D-02) that only bites if the right object is rated,
*we chose* to rate the integrated authenticated service at the required configuration as the headline, with mandatory, non-averaged sub-ratings and a weakest-link cap,
*to achieve* a KDP-0B gate that tests the actual gap (fleet scale, outage recovery and command authentication) while still crediting real heritage,
*accepting* a low headline (TRL 3) that may be read as unfair to mature RF, a funded Phase 0A demonstration costing several years of effort, and the risk that a later-found SDLS flight record shows we were over-conservative on one sub-element.

### Toulmin structure

- **Claim:** headline T26 is TRL 3 (4 conditional) and is gated at TRL 6 at KDP-0B.
- **Grounds:** no integrated article exists; the authentication and key-lifecycle evidence is uncited; the node gap is 2–4×.
- **Warrant:** the brief requires rating at the required scale, environment and duration. NASA TRL criteria attach to a stated configuration. A service fails at its weakest critical function, so averaging misrepresents it.
- **Backing:** NPR 7123.1 TRL definitions; the brief's "cite or say unsure" rule; the panel's own agreement on where the gap lies.
- **Qualifier:** *probably* correct. Moderate confidence on the object choice; low confidence on the precise headline number.
- **Rebuttal conditions:**
  - A cited deep-space key-management record moves the headline to 4.
  - A ruling that ground testbeds are not a relevant environment moves the TRL 6 path later.
  - If D-03 is resolved with no licence linkage *and* a degraded command mode exists, the risk class stays architecture-change and the TRL 6 gate could relax to TRL 5 plus a funded plan.

## 9. Consequences

**Decisions this enables:**
- The **next WP-A gate-design step** can list T26 explicitly, with a testable criterion rather than an argument about which number to believe.
- A **traffic budget work item** becomes mandatory and urgent. It blocks T26 qualification and probably others, such as autonomy and site-plant telemetry.
- An **SEL1 solar-exclusion analysis** feeds both T26 and the SEL1 node orbit selection. The halo amplitude may become a comms-driven requirement.
- An **evidence hunt** is commissioned: a targeted literature and agency search for flight use of SDLS or equivalent with on-orbit rekeying. It reports "found and cited" or "not found." Gemini's claim either earns a citation or is struck from the record.
- A **costed testbed plan** for the integrated demonstration is produced in Phase 0A. If Phase 0A is shorter than about 3 years, T26 joins the critical path.

**Decisions this constrains:**
- **Other composites** (e.g. any autonomy stack, power-and-thermal systems, ISRU chains) must follow the same object rule and cap. Some will drop from their current headline ratings. That is intended.
- **Architecture options that assume Earth-in-loop command** for tug high-energy operations are disfavoured until T26 matures, which reinforces the "no Earth-dependent safety action" requirement.
- **D-03 negotiation** gets an input: the project can offer the integrated demonstration and the assurance case as the licence evidence package, rather than waiting for the licensing state to define one.

**Disagreement kept, not averaged.**
- Gemini's position, that TRL 6 is met, is recorded as a dissent conditional on an SDLS deep-space citation.
- Claude's upper bound of 7 is recorded as valid only under the MRN-as-prototype interpretation, which this decision rejects.
- O5, splitting T26, remains a live alternative if the project prefers technology-level granularity, *provided* integration is assigned an owner.