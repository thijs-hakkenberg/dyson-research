# Zenodo Archival & Data/Code Availability — Project Dyson

**Purpose.** This is the shared Wave A blocker: every manuscript needs a
citable, versioned code/data archive with a DOI before submission. This guide
takes the repo from "code lives on GitHub" to "a tagged release is minted on
Zenodo with a DOI you can drop into each paper."

Prepared as part of Wave A submission prep. Two metadata files ship alongside
this guide:

- `.zenodo.json` — controls the Zenodo deposit's metadata on the GitHub→Zenodo
  automatic-release path (workspace copy is named `zenodo.json`; **rename to
  `.zenodo.json` at the repo root when deploying**).
- `CITATION.cff` — GitHub renders a "Cite this repository" button from this and
  it feeds reference managers.

---

## 0. Resolve two blockers first

1. **License mismatch (must fix before minting a DOI).**
   Repo root `LICENSE` = **GPL-3.0**, but `publications/scripts/pyproject.toml`
   declares `license = {text = "MIT"}`. A DOI'd release must state one coherent
   license. Decide which is intended:
   - If the whole project is GPL-3.0 → change the pyproject line to
     `license = {text = "GPL-3.0-or-later"}`.
   - If the analysis scripts are deliberately MIT (more permissive, common for
     research code so others can reuse it) → keep pyproject MIT, but add a note
     in the archive README that scripts are MIT-licensed while the web platform
     is GPL-3.0, and set the Zenodo `license` to the one covering the archived
     payload. The current `.zenodo.json`/`CITATION.cff` default to
     `GPL-3.0-or-later`; switch to `MIT` if that's the real intent for the
     archived scripts+data.

2. **Fill the placeholders** (marked `<FILL: ...>`) in both metadata files:
   - ORCID for Thijs Hakkenberg (get one free at orcid.org — reviewers
     increasingly expect it).
   - `version` / release tag — see §2.

---

## 1. What gets archived

Zenodo will snapshot the **entire repository** at the tagged commit (that's how
the GitHub integration works). That's fine — the payload the papers care about:

| Component | Path | Papers it supports |
|---|---|---|
| Analysis + simulation code (33 scripts, incl. tests) | `publications/scripts/` | all |
| ISRU Monte-Carlo model | `isru_mc.py`, `isru_model.py`, `extended_copula_sensitivity.py` | 01 |
| Swarm coordination / TDMA / NS-3 | `swarm_mc.py`, `packet_level_tdma.py`, `tdma_slot_sim.py`, `generate_ns3_validation_fig.py` | 02 |
| Multi-model deliberation analysis | `deliberation_analysis.py`, `transcript_similarity.py` | 03 |
| Water extraction MC | `water_extraction_mc.py`, `water_extraction_model.py` | 05 |
| Controlled baselines + repeated trials + ablations | `publications/data/` (254 files) | 01, 02, 03 |
| Pinned dependencies | `publications/scripts/requirements.txt` | reproducibility |

If you'd rather archive **only** `publications/` (not the SvelteKit web app),
that requires either a separate archive-only repo or a manual Zenodo upload
(§3, Option B) — the automatic path always takes the whole repo.

---

## 2. Minting the DOI — recommended path (GitHub → Zenodo)

This gives you a **concept DOI** (always resolves to the latest version) plus a
**version DOI** (this exact release). Cite the version DOI in papers.

1. Log in to **zenodo.org** with GitHub (OAuth).
2. **Settings → GitHub**, flip the toggle **ON** for `thijs-hakkenberg/dyson`.
   (Zenodo only sees releases created *after* the toggle is on.)
3. Commit `.zenodo.json` and `CITATION.cff` to the repo root (see §4).
4. On GitHub, **Releases → Draft a new release**:
   - Tag: `v0.1.0-wave-a` (or your scheme — put the same string in both metadata files' `version`).
   - Title: "Project Dyson — Wave A submission release".
   - Publish.
5. Zenodo auto-ingests within ~a minute and mints the DOI. Grab both the
   concept and version DOIs from the Zenodo deposit page.
6. Add the DOI badge to `README.md`:
   `[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)`

**Re-releasing:** each new GitHub release → new version DOI under the same
concept DOI. So you can cut `v0.1.0-wave-a` now for Papers 01/03 and a later
tag when Papers 02/04/05 submit; each paper cites the version current at its
submission.

---

## 3. Alternative paths

- **Option B — manual upload (archive only `publications/`):** zip
  `publications/scripts/` + `publications/data/` + a short README, upload at
  zenodo.org/deposit, paste the same metadata by hand. Use this only if you
  want to exclude the web app from the archive. You lose the automatic
  version-on-release convenience.
- **Option C — OSF or Figshare:** equivalent DOIs; use only if you already have
  an account there. Zenodo is the field default for space-systems/CS venues and
  is free with no size worry at this scale.

---

## 4. Deploying the metadata files

From the repo root:

```bash
# rename the workspace copy to the dotfile Zenodo expects
mv zenodo.json .zenodo.json      # (this guide ships it as zenodo.json)
git add .zenodo.json CITATION.cff
git commit -m "metadata: Zenodo deposit config + CITATION.cff for DOI archival"
```

Then validate the CFF (optional but catches typos):
```bash
pipx run cffconvert --validate      # or: pip install cffconvert && cffconvert --validate
```

---

## 5. Per-paper "Data and Code Availability" statements

Drop the matching block into each manuscript. Replace `10.5281/zenodo.XXXXXXX`
with the **version DOI** from §2. These are written to satisfy the availability
requirements of the target venues (Advances in Space Research, IEEE T-AES,
Systems Engineering, Acta Astronautica, J. Spacecraft & Rockets).

### Paper 01 — ISRU Economic Crossover (Advances in Space Research)
> **Data and Code Availability.** The Monte-Carlo economic model, sensitivity
> analyses, and figure-generation scripts are openly available in the Project
> Dyson archive (Zenodo, DOI: 10.5281/zenodo.XXXXXXX), with source under version
> control at https://github.com/thijs-hakkenberg/dyson. The crossover analysis
> is reproduced by running `publications/scripts/isru_mc.py` and
> `generate_isru_figures.py` against the archived controlled-baseline and
> repeated-trial datasets under `publications/data/`; dependencies are pinned in
> `requirements.txt`.

### Paper 02 — Swarm Coordination Scaling (IEEE T-AES)
> **Data and Code Availability.** The packet-level TDMA simulator, NS-3
> validation harness, and analysis scripts are openly available in the Project
> Dyson archive (Zenodo, DOI: 10.5281/zenodo.XXXXXXX;
> https://github.com/thijs-hakkenberg/dyson). Coordination-scaling results and
> the NS-3 cross-validation figure are regenerated via
> `publications/scripts/packet_level_tdma.py`, `tdma_slot_sim.py`, and
> `generate_ns3_validation_fig.py`.

### Paper 03 — Multi-Model AI Consensus (Systems Engineering, INCOSE)
> **Data and Code Availability.** Deliberation transcripts, consensus/quality
> evaluations, controlled baselines, and winner-hidden ablation data are openly
> available in the Project Dyson archive (Zenodo, DOI: 10.5281/zenodo.XXXXXXX;
> https://github.com/thijs-hakkenberg/dyson). Analyses are reproduced with
> `publications/scripts/deliberation_analysis.py` and `transcript_similarity.py`
> over the datasets in `publications/data/controlled-baselines/`,
> `repeated-trials/`, and `winner-hidden-ablation/`. The exact model builds used
> in the deliberations are listed in the manuscript's model-provenance table.

### Paper 04 — Microgravity Metallurgy (Acta Astronautica)
> **Data and Code Availability.** Supporting analysis code and data are openly
> available in the Project Dyson archive (Zenodo, DOI: 10.5281/zenodo.XXXXXXX;
> https://github.com/thijs-hakkenberg/dyson).

### Paper 05 — ISRU Water Extraction (Acta Astronautica)
> **Data and Code Availability.** The water-extraction Monte-Carlo model and
> figure scripts are openly available in the Project Dyson archive (Zenodo, DOI:
> 10.5281/zenodo.XXXXXXX; https://github.com/thijs-hakkenberg/dyson), reproduced
> via `publications/scripts/water_extraction_mc.py` and
> `water_extraction_model.py`.

### Paper 11 — High-Voltage Architecture & Arc Management (J. Spacecraft & Rockets)
> **Data and Code Availability.** This is a synthesis/architecture study; no new
> simulation datasets are generated. Supporting literature-derived parameter
> tables are available in the Project Dyson archive (Zenodo, DOI:
> 10.5281/zenodo.XXXXXXX; https://github.com/thijs-hakkenberg/dyson).

---

## 6. Checklist

- [ ] Resolve GPL-vs-MIT license mismatch (§0.1)
- [ ] Get/confirm ORCID; fill `<FILL:>` in `.zenodo.json` and `CITATION.cff`
- [ ] Choose release tag; put identical string in both files' `version`
- [ ] Rename `zenodo.json` → `.zenodo.json`; commit both metadata files
- [ ] Enable Zenodo↔GitHub for the repo (§2.2)
- [ ] Draft & publish the GitHub release
- [ ] Copy concept + version DOIs from Zenodo
- [ ] Add DOI badge to README
- [ ] Paste the version DOI into each paper's Data & Code Availability block
