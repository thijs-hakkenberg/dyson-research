# Framework-mode deliberations (rq-0-64 … rq-0-75)

Twelve multi-model deliberations run in **decision-framework mode** on 2026-10-17. Each model
answered an owner-level governance question by applying a written decision framework
([`decision-frameworks.md`](decision-frameworks.md), body sha256 prefix `18f503fe4ec6`), with
blind voting, hidden winners and full prior context. The questions are the owner rulings needed
before Project Dyson's Phase 0 TRL re-baseline gates can be finalised: one on what the
communications TRL rates (rq-0-64), and eleven on the gate proposal (rq-0-65 … rq-0-75).

For **Paper 03 (Multi-Model AI Consensus)**, this is the first dataset where:

- the models deliberate on *decision rules* under an explicit framework, not on engineering
  specifications;
- every question has a **second, independent synthesis** of the same transcripts by a different
  model, so synthesizer bias can be measured;
- an owner then acted on the result (`owner-rulings.yaml`).

## Panel and method

| | |
|---|---|
| Models | Claude Opus 5.5, Gemini 3.1 Pro, GPT-6.1 Sol (Databricks AI Gateway) |
| Mode | framework (`decision-frameworks.md`), blind voting, hidden winner, full prior context |
| Termination | unanimous CONCLUDE, max 5 rounds, self-vote weight 0.5 |
| Primary synthesizer | GPT-6.1 Sol (all 12) |
| Alternate synthesizer | Claude Opus 5.5 (rq-0-65 … rq-0-75, `--resynthesize` on the same transcripts) |
| Orchestrator | `scripts/run-discussion.js` in [thijs-hakkenberg/dyson](https://github.com/thijs-hakkenberg/dyson); file hashes per run in each `provenance.yaml` |

## Findings

1. **Every deliberation stopped after one round.** All twelve ended on a unanimous CONCLUDE vote
   in round 1. Framework mode produced no critique rounds.
2. **Win concentration.** GPT-6.1 Sol's response won 9 of 12 rounds (Claude 3, Gemini 0), and
   GPT also wrote all 12 primary syntheses. That is why the alternate synthesis was run.
3. **Neither synthesizer favoured its own model; both overstated convergence toward the other's
   position.** Checked against the round-1 responses:
   - rq-0-67: the alternate (Claude) declared the economics-premium question resolved for all
     three models; Claude's own response allowed a pre-authorised premium to produce a pass.
   - rq-0-72: the primary (GPT) declared convergence on Claude's composite-TRL rule; GPT had
     voted APPROVE, but its own written rule differs.
4. **Mechanism.** The synthesizers read an APPROVE vote on another model's response as agreement
   with that response's rule. In the framework-mode rubric, APPROVE means "the decision chain
   (frame, alternatives, information, values, reasoning, commitment) has no weak link that would
   change the decision". That judges the reasoning; it does not adopt the rule.
5. **Validated convergence is rare.** Only 3 of 11 gate questions converged by the strict test
   (both syntheses agree and the round-1 responses bear it out): rq-0-68, rq-0-70 and the core of
   rq-0-74. Two more share a direction (rq-0-69, rq-0-73). The owner confirmed the eight
   converged points (`owner-rulings.yaml`) and routed the rest to evidence questions.

Proposed pipeline fixes (not yet made at the time of archiving): require at least two rounds in
framework mode, and have the synthesizer quote each model's own rule text before declaring
convergence.

## Layout

```
summary.json                      per question: method, config, round scores, termination votes,
                                  synthesizers, convergence verdict (machine-readable)
ruling-syntheses-comparison.md    primary vs alternate synthesis, checked against round-1 responses
owner-rulings.yaml                what the owner confirmed (2026-10-20)
decision-frameworks.md            the framework the models applied (body sha 18f503fe4ec6)
questions/<rq-id>-<slug>/
  question.md                     the question as posed, with its status note
  discussion.yaml                 full deliberation record (responses, votes, termination)
  round-1/<model>.md, votes.yaml  responses and blind votes
  conclusion.md                   primary synthesis (GPT-6.1 Sol)
  conclusion.claude-opus-5-5.md   alternate synthesis (Claude Opus 5.5)
  divergent-views*.yaml           extracted divergent views, per synthesizer
  provenance.yaml                 orchestrator commit, file hashes, models, endpoints
raw-exchanges/<slug>/<model>/     every LLM request and response (project-dyson/llm-exchange@1);
                                  hosts redacted, no credentials
```

## Reproducing the counts

```python
import json
s = json.load(open('summary.json'))
for q in s['questions']:
    print(q['questionId'], len(q['rounds']), q['terminationReason'],
          q['rounds'][0]['winner'], q['convergenceVerdict'])
```

Source: `thijs-hakkenberg/dyson` at `1dd770f` (PR #12) and PR #14 (owner rulings). License: MIT,
as for the rest of this repository.
