# Version AM Peer Review Summary

| Reviewer | Recommendation | Key Issues |
|----------|---------------|------------|
| Gemini 3 Pro | **Accept** | C_mat notational collision (proofs-stage), config table n_v column, commit hash |
| GPT-5.2 | **Accept** | Commit hash, material cost $540/kg clarification, Table 6 formatting, asymptotic f_v notation |
| Claude Opus 4.6 | **Minor Revision** | Abstract "both forms tested deterministically" wording (FIXED in-place), recrossing table % basis footnote (FIXED in-place), commit hash |

## Consensus Issues (2+ reviewers)

1. **Commit hash still PENDING** (all three) — Must be resolved before publication. Administrative item.

## Post-Review In-Place Fixes Applied

Two Claude concerns were fixed directly in AM without a new version:
1. Abstract: "both forms are tested deterministically only" → "the comparison is deterministic, and only the piecewise plateau is integrated into the stochastic MC"
2. Recrossing table: "6,622 (66.2%)" → "6,622 (66.2% of total; 77.8% of converging)"

## Remaining Individual Issues (cosmetic only)

- **C_mat notational collision** (Gemini) — C_mat = $1M in Eq. 2 vs C_mat = m·p_fuel = $0.37M in Eq. 13. Proofs-stage fix.
- **Config table n_v column** (Gemini) — n_v should appear in Baseline MC column
- **Material cost $540/kg clarification** (GPT) — Clarify as effective/certified cost
- **Table 6 formatting** (GPT) — Mix of absolute/percentage shifts
- **Asymptotic f_v vs f_v^floor** (GPT) — Notation precision in displayed expression

## Progress

- AL → AM changes: abstract split, logistic equation numbered, C_floor^labor → C_mat, K-median Det.N* "(lump)", yield/logistic deterministic-only acknowledged, permanent/transient % unified, Eq.20 labeled as t₀=5 case, dual σ_ln in abstract
- Gemini: Accept → **Accept** (stable)
- GPT: Minor → **Accept** (all minor concerns resolved)
- Claude: Minor → **Minor** (one sentence fix applied in-place → effectively Accept)

## Status

**Paper is ready for submission** pending commit hash resolution. All three reviewers at Accept or Accept-equivalent. No Major or substantive Minor concerns remain. Remaining issues are cosmetic/proofs-stage items.
