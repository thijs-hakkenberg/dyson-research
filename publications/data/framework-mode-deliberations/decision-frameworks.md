---
slug: decision-frameworks
title: Trade-off Decision Frameworks
type: methodology
summary: Reference of mature trade-off methods (ATAM, GRADE EtD, QOC, ACH, Toulmin…) and the composite scaffold every critique round of a re-assessment applies to the decisions it reviews.
usedBy:
  - scripts/run-reassessment.js (critique rounds, --prior-round)
---

# Trade-off Decision Frameworks — Reference

Mature methodologies for structuring trade-off decisions, drawn from architecture, decision science, medicine, intelligence analysis and safety engineering. Use as a menu to test in parallel against real decisions.

---

## 1. Systems & Software Architecture

| Method | Core idea | What to steal |
|---|---|---|
| **ATAM** (SEI, Kazman) | Evaluate architecture against quality-attribute scenarios via a utility tree | **Sensitivity point** = decision strongly affecting one attribute. **Trade-off point** = decision affecting two attributes in opposite directions. Naming which one you're at removes most of the fog. |
| **CBAM** | ATAM + economics | Attach cost, benefit and uncertainty ranges to each branch of the utility tree |
| **Tyree & Akerman** (IEEE Software, 2005) | Rich ADR template | Issue, assumptions, constraints, **positions** (rejected options with argument), implications, related decisions |
| **Y-statements** (Zimmermann) | One-sentence decision record | *In the context of X, facing Y, we chose Z, to achieve W, accepting V* |
| **Kruchten decision ontology** | Decision taxonomy + relations | Existence / property / executive decisions; relations: constrains, enables, subsumes, conflicts |
| **ISO/IEC/IEEE 42010** | Architecture description standard | Decisions and rationale are first-class elements, not commentary |

---

## 2. Decision Analysis (the parent discipline)

- **Howard/Raiffa decision basis** — every decision = what you *know* + what you *can do* + what you *want*. Bad write-ups collapse these three.
- **Decision Quality chain** (Spetzler) — frame · alternatives · information · values · reasoning · commitment. Quality = weakest link. Use as an audit checklist.
- **Value-Focused Thinking** (Keeney) — establish values/criteria *before* generating alternatives. Otherwise you only evaluate what was handed to you.
- **Even swaps** (Hammond, Keeney, Raiffa) — neutralise attributes one at a time to make options directly comparable. No tooling required.
- **Kepner-Tregoe Decision Analysis** — **musts** (binary screening) vs **wants** (weighted scoring), then an explicit adverse-consequences pass.

---

## 3. Multi-Criteria Decision Analysis (MCDA)

- **AHP** (Saaty) — pairwise comparison with a consistency ratio check
- **MAUT / SMART** — utility functions with **swing weights** (weights must reference the actual range of each criterion)
- **TOPSIS** — rank by distance to ideal and anti-ideal solutions
- **Outranking school** — ELECTRE, PROMETHEE (Bernard Roy)

> Roy's framing: MCDA **structures a debate**, it does not compute a truth. Good default posture for vendor comparisons.

---

## 4. Design Rationale — closest fit to "help me make this trade-off"

- **QOC** (Questions, Options, Criteria) — a small formal grammar: options assessed against criteria, criteria stated separately from options. Maps almost directly onto a prompt template.
- **IBIS / dialogue mapping** (Rittel, Conklin) — issue → positions → arguments pro/con. Built for wicked problems.
- **Toulmin argument model** — claim · grounds · **warrant** · backing · qualifier · rebuttal. The missing *warrant* (why the grounds support the claim) is why most ADRs feel hand-wavy.

---

## 5. Science & Evidence

- **GRADE Evidence-to-Decision** (medicine) — arguably the best structured trade-off template in existence. Rates separately: benefits vs harms, certainty of evidence, values, resource use, equity, acceptability, feasibility — *before* stating a recommendation.
- **IPCC calibrated language** — separate **likelihood** from **confidence**; confidence derived from evidence quality × degree of agreement.
- **Multiverse / specification-curve analysis** — report the conclusion across *all* defensible analytic choices instead of one path.
- **Strong inference** (Platt) — design each step to discriminate between competing hypotheses.
- **Structured expert elicitation** — Cooke's classical method, SHELF, Delphi.

---

## 6. Intelligence Analysis

- **ACH** (Analysis of Competing Hypotheses, Heuer) — score evidence against *all* hypotheses; seek **disconfirmation**; rank by least-disconfirmed.
- **ICD 203 analytic standards** — mandates calibrated probability language, explicit assumptions, and separation of judgment from sourcing.
- **Key assumptions check**, **premortem** (Klein), **red team / devil's advocacy**.

---

## 7. Safety & Assurance Engineering

- **Assurance cases with GSN** — goal → strategy → solution, with **context** and **assumptions** as explicit graph nodes. Toulmin made diagrammatic; excellent at forcing "what would have to be true".
- **ALARP** — reduce risk until further reduction is grossly disproportionate to benefit.
- **STPA**, **FMEA** — systematic hazard and failure-mode enumeration.

---

## 8. Business & Economics

- **Cost of Delay / CD3** (Reinertsen) — quantify the cost of *not* deciding
- **Real options / deferral value** — what is it worth to decide later with more information
- **Reversibility** — one-way vs two-way doors; match rigour to reversibility
- **Wardley mapping** — situational awareness *before* choosing
- **RAPID / DACI** — decision rights, separate from decision content
- **Cynefin** — match method to problem type (clear / complicated / complex / chaotic)

---

## Composite Scaffold

A synthesis to test as an ADR template or prompt fragment:

1. **Frame & decision type** — reversible? existence / property / executive? Cynefin domain?
2. **Criteria and weights** — stated *before* options *(Value-Focused Thinking, swing weights)*
3. **Options** — including the null option and rejected ones with argument *(Tyree)*
4. **Assessment matrix** — options × criteria *(QOC)*
5. **Sensitivity vs trade-off points** — named explicitly *(ATAM)*
6. **Evidence certainty** — per claim, calibrated *(GRADE, ICD 203)*
7. **Key assumptions** — and what would falsify each *(ACH, premortem)*
8. **Decision, warrant, accepted downside** *(Y-statement, Toulmin)*
9. **Consequences** — and follow-on decisions unlocked or constrained *(Kruchten)*

---

## Suggested Parallel Test

Run the same real decision through three at once — they fail in different ways and the disagreement is the signal:

- **QOC** — fast, low ceremony, good for small decisions
- **GRADE EtD** — heavy, but exposes weak evidence and unstated values
- **ACH** — best when you suspect you've already anchored on an answer
