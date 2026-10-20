# Gate rulings (rq-0-65 … rq-0-75): primary vs alternate synthesis

*2026-10-18. Primary synthesizer GPT-6.1 Sol (`conclusion.md`, `divergent-views.yaml`); alternate
Claude Opus 5.5 (`conclusion.claude-opus-5-5.md`, `divergent-views.claude-opus-5-5.yaml`), run with
`--resynthesize` on the same transcripts, votes and framework (18f503fe4ec6). Reason: GPT's response
won 8 of 11 rounds while GPT also synthesised all 11.*

## Finding

Neither synthesizer favoured its own model. Both **overstated convergence**, each time toward the
other model's position, and each was caught by checking the round-1 responses:

| Question | Primary (GPT) | Alternate (Claude) | Round-1 responses | More accurate |
|---|---|---|---|---|
| rq-0-67 economics premium | Split: Claude alone lets a pre-authorised premium produce a gate pass; Gemini and GPT do not | "Resolved" for all three: a premium "is not an economics pass" | Claude's response: the gate "passes only if parity holds, **or** if the premium is within both caps" | **Primary** |
| rq-0-72 composite TRL | "Converged" on Claude's bounded integration rule | Partial: GPT's written rule differs on reconciling lower ratings | GPT voted APPROVE on Claude's rule, but its own rule does "not … automatically inherit [the] minimum" and allows scope-distinction reconciliation | **Alternate** |

## Where the two syntheses agree

| Question | Agreed by both syntheses |
|---|---|
| rq-0-68 demand terms | Converged core: "within 3×" is a quantity ratio; "signed" means specified, financially backed commitments. Capacity authorised after a pass is open. |
| rq-0-70 licence reapplication | Converged: at most one bounded redesign and reapplication for a remediable failure, requirements unchanged. Window length open. |
| rq-0-74 D-02 for flight projects | Shared core: tranche releases are two-way (TRL 4–5); a scout or pathfinder PDR is a separate gate needing TRL 6 for flight-critical technology. Exceptions and amend-vs-interpret open. |
| rq-0-69 sunset | Shared direction: automatic fallback at M180; exception and re-entry rules differ by model. |
| rq-0-73 scout milestone | TRL 6 at scout PDR; pre-launch level and the target-gate evidence differ. |
| rq-0-66, 71, 75 | No convergence; three positions each. |

rq-0-65 (risk classes): the alternate finds a Claude–GPT core (project-ending unless an independently
reviewed fallback package is accepted); the primary lists three positions. Treat as not converged
until the owner reads both.

## Rule for the owner rulings

Count a ruling as converged only where **both** syntheses report it and the round-1 responses bear it
out: rq-0-68, rq-0-70 and the shared core of rq-0-74 (and the direction of rq-0-69, rq-0-73). Read the
others as positions.

## Pipeline note

Framework-mode discussions all stopped after one round (unanimous CONCLUDE), and synthesizers
over-read APPROVE votes as agreement with the approved response's rule. Two candidate fixes, not yet
made: require at least two rounds in framework mode, and have the synthesizer quote each model's own
rule text before declaring convergence.
