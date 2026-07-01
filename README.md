# Project Dyson — Research

Simulation code, analysis scripts, research data, and manuscripts for the
**Project Dyson** publication series: an open, multi-model AI-consensus
engineering-planning program for a Dyson swarm.

This repository is the **research archive** — the citable, reproducible half of
Project Dyson. The interactive planning platform (SvelteKit web app) lives
separately at [`thijs-hakkenberg/dyson`](https://github.com/thijs-hakkenberg/dyson)
under GPL-3.0. This split lets the research artifacts carry a permissive **MIT**
license (maximizing reuse and replication) without entangling the web
application's copyleft.

- Project site: https://project-dyson.pages.dev/
- Web platform repo: https://github.com/thijs-hakkenberg/dyson

## Layout

```
publications/
├── drafts/            # manuscripts (papers 01–11), each with review rounds
├── scripts/           # simulation + analysis code (MIT), pinned deps
│   ├── requirements.txt
│   └── tests/         # pytest suite
├── data/              # deliberation datasets, controlled baselines,
│                      #   repeated trials, ablations
├── figures/           # generated figures
research/              # literature corpus, research-question maps, gap analyses
.zenodo.json           # Zenodo deposit metadata (DOI on GitHub release)
CITATION.cff           # "Cite this repository"
```

## Reproducing results

```bash
cd publications/scripts
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest                          # run the test suite
python isru_mc.py               # e.g. regenerate ISRU Monte-Carlo results
python generate_isru_figures.py # regenerate paper-01 figures
```

Each paper's "Data and Code Availability" statement names the exact scripts
that reproduce its results (see `publications/zenodo-archival-guide.md`).

## Papers (publication series)

| # | Title | Target venue |
|---|-------|--------------|
| 01 | ISRU Economic Crossover | Advances in Space Research |
| 02 | Swarm Coordination Scaling | IEEE T-AES |
| 03 | Multi-Model AI Consensus | Systems Engineering (INCOSE) |
| 04 | Microgravity Metallurgy | Acta Astronautica |
| 05 | ISRU Water Extraction | Acta Astronautica |
| 06 | Cryogenic Propellant Architecture | Cryogenics |
| 10 | Thin-Film Deposition | J. Applied Physics |
| 11 | High-Voltage Architecture & Arc Management | J. Spacecraft & Rockets |

## Model provenance

Deliberations and multi-model consensus (Papers 02, 03) used the February 2026
model generation: **Claude Opus 4.6**, **Gemini 3 Pro**, **GPT-5.2**. Paper 01's
later review rounds additionally used the May 2026 generation (Claude Opus 4.7,
Gemini 3.1 Pro, GPT-5.5 Pro). See `publications/model-provenance-reconciliation.md`.

## License

MIT — see [LICENSE](LICENSE). The Project Dyson web platform is separately
licensed under GPL-3.0.

## Citation

If you use this code, data, or the research outputs, please cite the archive via
the DOI on the Zenodo release (see `CITATION.cff`).
