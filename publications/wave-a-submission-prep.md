# Wave A — Submission Prep Pack

_Concrete, reusable materials to move Papers 01 and 03 from complete-draft to submitted. Prepared without editing the live manuscripts: **Paper 01 is mid-revision to v.AQ** (active Monte-Carlo re-run cycle), so its citation edits are staged here as instructions to apply once v.AQ settles, not as direct edits._


## A. Reusable AI-contribution disclosure statement

Drop-in paragraph for the end of each manuscript (adjust venue-specific wording). Every Project Dyson paper uses AI models both as analysis instruments and as structured reviewers, so disclosure must be explicit and uniform across the portfolio.

> **AI-contribution disclosure.** This work used large language models (LLMs) in two distinct roles.
> (1) *As analysis instruments:* models were used to draft prose, generate and check code, and structure
> multi-model trade studies; all quantitative results derive from explicitly specified simulation code and
> data, which are archived and citable (see Data & Code Availability). (2) *As structured reviewers:* draft
> versions were iteratively critiqued by multiple independent models under a fixed rubric, and revisions were
> made by the authors in response. No LLM is an author; the authors take full responsibility for all claims,
> analyses, and conclusions. Exact model identifiers, versions, and dates are listed in the reproducibility
> appendix. Human authors designed the studies, verified all numerical results against source code, and
> approved the final manuscript.


## B. Model-version freeze table (Paper 03, and portfolio-wide)

The holistic review found inconsistent model naming across documents (e.g. Claude 4.6 vs 4.7, GPT-5.2 vs 5.5, `gpt4`/`GPT-4` mixed with `GPT-5.2`, `gemini-3-pro` vs `Gemini 3 Pro`). **Before submitting Paper 03, pin one canonical table and use it verbatim everywhere.** Fill the exact build IDs/dates from the deliberation logs — placeholders below must be replaced with the actual values, not guessed:

| Role in study | Vendor family | Canonical name (use verbatim) | Exact model ID | Version/build | Access date |
|---|---|---|---|---|---|
| Reviewer / participant A | Anthropic | Claude (Opus) | `<fill: e.g. claude-opus-4-...>` | `<fill>` | `<fill>` |
| Reviewer / participant B | OpenAI | GPT | `<fill: e.g. gpt-5-...>` | `<fill>` | `<fill>` |
| Reviewer / participant C | Google | Gemini (Pro) | `<fill: e.g. gemini-3-...-pro>` | `<fill>` | `<fill>` |

**Action for Paper 03:** grep the manuscript for every model mention (`claude`, `gpt`, `gpt4`, `GPT-4`, `GPT-5.2`, `gemini`, `Gemini 3 Pro`) and replace with the canonical-name column; move all raw IDs/dates into a single reproducibility appendix that points at the deliberation-log commit hash.


## C. Paper 01 — citation additions (apply after v.AQ)

Paper 01's bibliography (1936–2023) is thin on recent space-economics literature. The crossover claim is timely precisely because launch costs are moving, so the recency of the cost anchors matters to reviewers. **Honest finding:** most launch-cost evidence is primary/grey (operator price sheets, CBO/FAA/GAO reports, NASA cost models), not journal articles — cite those directly as primary data. The two journal-citable additions worth adding:

- Ding et al. (2021). *The economics of additive manufacturing: Towards a general cost model including process failure*. International Journal of Production Economics. [10.1016/j.ijpe.2021.108087](https://doi.org/10.1016/j.ijpe.2021.108087)
- Kim et al. (2025). *Counting stars and costs: An empirical examination of space launch cost trend at NASA*. Acta Astronautica. [10.1016/j.actaastro.2025.04.011](https://doi.org/10.1016/j.actaastro.2025.04.011)

**Recommended primary/grey anchors to cite explicitly** (verify latest figures at submission time):
- Operator-published $/kg to LEO for current reusable vehicles (cite as primary source with access date).
- A government cost-analysis reference (e.g. CBO/GAO launch-cost analysis) for an independent baseline.
- NASA's published in-space-manufacturing / ISRU cost-model documentation for the ISRU-side parameters.
**Do not** substitute weak journal proxies for these — a reviewer in *Advances in Space Research* will prefer a dated primary figure over a tangential citation.


## D. Per-paper submission checklist

**Paper 01 → Advances in Space Research**
1. Finish v.AQ Monte-Carlo re-run cycle (in progress).
2. Add the recent cost anchors (Section C).
3. Convert citations to ASR (Elsevier) style; verify every DOI resolves.
4. Append AI-disclosure (Section A) + reproducibility appendix.
5. Archive simulator + MC notebooks to Zenodo; cite the versioned DOI.
6. State pre-Phase-A feasibility framing in the intro.

**Paper 03 → Systems Engineering (INCOSE) [primary] / IEEE Intelligent Systems [backup]**
1. Apply the model-version freeze table (Section B) verbatim throughout.
2. Add reproducibility appendix (model IDs/dates + deliberation-log commit hash).
3. Append AI-disclosure (Section A).
4. Confirm the venue's LLM-in-methodology policy before submission (some venues are wary of LLM-as-reviewer framing).
5. Archive `aggregation-baseline-results.json` + `self-refinement-results.json` with the code release.


---
_Blocking item common to both: a Zenodo (or equivalent) code/data archive with a release tag, cited by DOI. This is the single highest-leverage pre-submission task and unblocks the Data & Code Availability statement both papers need._
