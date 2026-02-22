# Version AL Peer Review Summary

| Reviewer | Recommendation | Key Issues |
|----------|---------------|------------|
| Gemini 3 Pro | **Accept** | Abstract CI rounding, K-median Det. N* column clarification, logistic needs equation number, yield not in MC |
| GPT-5.2 | **Minor Revision** | Eq. 20 vs Eq. 8 phased capex notation, K-median Det. N* column header, logistic exponent justification, commit hash |
| Claude Opus 4.6 | **Minor Revision** | Permanent/transient percentage framing, logistic not tested stochastically, yield not in MC, abstract density |

## Consensus Issues (2+ reviewers)

1. **K-median sweep Det. N* column ambiguity** (all three) — Column uses lump-sum K at median value, not phased K at $50B. Needs caption/header clarification.
2. **Yield parameter not in MC** (Gemini, Claude) — Y is deterministic only; consider adding Y ~ U[0.85, 1.0] to MC or explicitly noting omission.
3. **Logistic form tested only deterministically** (Gemini, Claude) — Plateau is stochastic in MC; logistic is deterministic only. Acknowledge asymmetry.
4. **Commit hash still PENDING** (all three) — Must be resolved before publication.
5. **Logistic formula needs equation number** (Gemini, GPT) — Currently inline; should be numbered for cross-referencing.

## Individual Issues

- **Eq. 20 vs Eq. 8 inconsistency** (GPT only) — Eq. 20 shows uncoupled form; Eq. 8 shows coupled
- **Permanent/transient % framing** (Claude only) — Body uses % of total; abstract uses % of converging
- **Abstract density/split** (Claude only) — Single paragraph too dense; consider splitting into two
- **Config table vitamin row** (Gemini only) — n_v should appear in Baseline MC column, not just Sensitivity
- **$C_{\mathrm{floor}}^{\mathrm{labor}}$ undefined** (Claude only) — Logistic formula uses undefined term
- **Material cost $540/kg** (GPT only) — Clarify as effective/certified cost, not commodity price

## Progress

- AK → AL changes: logistic comparison, yield parameter, K-median sweep to main text, KM to main text, phased capex equation, stale table fixes
- Gemini: Accept → **Accept** (stable)
- GPT: Major → **Minor** (all 5 major concerns resolved)
- Claude: Major → **Minor** (all 4 major concerns resolved)

## Priority for Version AM (if desired)

1. Fix K-median Det. N* column header (consensus)
2. Add logistic saturation as numbered equation (consensus)
3. Add sentence acknowledging logistic/yield are deterministic-only (consensus)
4. Reconcile Eq. 8 and Eq. 20 phased capex notation (GPT)
5. Fix permanent/transient % framing (Claude)
6. Update commit hash (all)
