# Version AK Peer Review Summary

| Reviewer | Recommendation | Key Issues |
|----------|---------------|------------|
| Gemini 3 Pro | **Accept** | K mass-budget sanity check, launch cost vs price terminology |
| GPT-5.2 | **Major Revision** | Inconsistent MC numbers across appendix tables, KM promotion, alternative learning curve form, capex equation inconsistency, K prior anchoring |
| Claude Opus 4.6 | **Major Revision** | K-median sweep as primary result, alternative saturating learning form, yield/reliability parameter, revenue block deployment |

## Consensus Issues (2+ reviewers)

1. **K reframing / conditional presentation** (GPT, Claude, Gemini) — All three reviewers note K is weakly grounded and dominates results. GPT and Claude want K-median sweep elevated to primary result. Gemini wants a mass-budget sanity check.

2. **Alternative learning curve saturation form** (GPT, Claude) — Both want at least one alternative (logistic, De Jong) tested alongside the piecewise plateau to assess model-form sensitivity.

3. **Inconsistent appendix table numbers** (GPT) — Copula table and possibly other appendix tables still show old convergence rates from pre-plateau runs. Must regenerate all tables from canonical pipeline.

4. **KM results promotion** (GPT) — Kaplan-Meier results should be in main text, not just appendix.

5. **Reproducibility** (GPT, Claude) — Commit hash "PENDING" not acceptable; need fixed hash.

## Individual Issues

- **Yield/reliability parameter** (Claude only) — Add $Y \in [0.7, 1.0]$ for ISRU manufacturing yield
- **Revenue block deployment** (Claude only) — Discuss block commissioning thresholds for SSP
- **Capex equation** (GPT) — Main NPV equation should show phased capex explicitly
- **Launch cost vs price** (Gemini) — Clarify commercial procurement vs cost-plus
- **Paper length** (Claude) — Wants 30-40% cut; GPT also notes density

## Progress

- AJ → AK changes: stochastic plateau in MC baseline, dynamic vitamin fraction, all table updates, recrossing fix
- Gemini: Accept → **Accept** (stable)
- GPT: Major → **Major** (same, new concern: table inconsistency)
- Claude: Major → **Major** (same, recurring K and learning curve concerns)

## Priority for Version AL

1. Fix all stale appendix tables (GPT Major #1) — regenerate from canonical pipeline
2. Implement logistic/De Jong alternative saturating form (GPT Major #3, Claude Major #2)
3. Reframe K presentation: K-median sweep as primary, headline as conditional (Claude Major #1, GPT Major #5)
4. Add yield parameter $Y$ (Claude Major #3)
5. Update NPV equation to show phased capex (GPT Major #4)
6. Promote KM to main text (GPT Major #2)
