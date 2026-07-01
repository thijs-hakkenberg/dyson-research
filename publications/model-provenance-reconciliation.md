# Model Provenance Reconciliation — Project Dyson

Derived from git history + embedded model IDs in the real repo
(`/Users/hakketh/projects/experiments/dyson`), 2026-07-01.
Reviewer filenames in each `reviews/version-*/` round ARE the model IDs;
per-file `git log --diff-filter=A` dates pin when each was used.

## Two generations, two time windows

### February 2026 generation  (canonical for deliberations + Papers 02, 03, early 01)
| Canonical name  | Repo ID string   | First commit |
|-----------------|------------------|--------------|
| Claude Opus 4.6 | `claude-opus-4-6`| 2026-02-22   |
| Gemini 3 Pro    | `gemini-3-pro`   | 2026-02-22   |
| GPT-5.2         | `gpt-5-2`        | 2026-02-22   |

### May 2026 generation  (Paper 01 later review rounds only; holistic-review 2026-05-11)
| Canonical name  | Repo ID string    | First commit |
|-----------------|-------------------|--------------|
| Claude Opus 4.7 | `claude-opus-4-7` | 2026-05-11   |
| Gemini 3.1 Pro  | `gemini-3-1-pro`  | 2026-05-11   |
| GPT-5.5 Pro     | `gpt-5-5-pro`     | 2026-05-11   |

## Per-artifact assignment
| Artifact | Models | Notes |
|----------|--------|-------|
| `publications/data/` (all deliberations, controlled-baselines, repeated-trials) | Feb trio | ground-truth data files: 1236 `claude-opus-4-6`, 1138 `gemini-3-pro`, 1132 `gpt-5-2` |
| `winner-hidden-ablation` | Feb trio (claude-opus-4-6, gpt-5-2 dominant) | ablation subset |
| Paper 02 (swarm coordination) | Feb trio | 119 review rounds, no May variants |
| Paper 03 (multi-model consensus) | **Feb trio** | 13 review rounds, no May variants — canonical table = these 3 |
| Paper 01 (ISRU crossover) | **BOTH** | drafted Feb 22 w/ Feb trio; reviewers upgraded to May trio from `version-am` (2026-05-11/12). `version-am` holds both sets; `version-ao`/`version-ap` hold only May trio |

## Normalization needed (Paper 03 freeze table)
These are all FORMATTING variants of the SAME 3 Feb-generation models, not different models:
- GPT-5.2  ← `gpt-5-2`, `gpt-5.2`, `GPT-5.2`, (stray `gpt-4`/`gpt4` = casual prose, NOT participants)
- Gemini 3 Pro ← `gemini-3-pro`, `Gemini 3 Pro`, `gemini 3`
- Claude Opus 4.6 ← `claude-opus-4-6`, `Claude Opus 4.6`, `claude 4.6`, `claude-opus-4`

## Recommended canonical strings (pick one style, apply everywhere)
- **Claude Opus 4.6**  (Anthropic)
- **Gemini 3 Pro**  (Google DeepMind)
- **GPT-5.2**  (OpenAI)

For Paper 01, if it names its review panel, cite both generations with the
version-am boundary, OR declare the final (May) trio as the official panel.
