# Project Dyson — Publication Scripts

Companion simulation and analysis code for the Project Dyson research papers.

## Modules

### Paper 01: ISRU Economic Crossover

| File | Purpose |
|------|---------|
| `isru_model.py` | Pure cost model (Eqs. 1-9 + NPV extensions). No I/O. |
| `isru_mc.py` | Monte Carlo engine: sampling, loop, statistics, PRCC. No I/O. |
| `generate_isru_figures.py` | Generates all 6 publication figures + diagnostic tables. |
| `extended_copula_sensitivity.py` | Appendix: 6-D copula sensitivity analysis (AE1). |

### Paper 02: Swarm Coordination Scaling

| File | Purpose |
|------|---------|
| `swarm_model.py` | Discrete-event simulator for swarm coordination (3 topologies). No I/O. |
| `swarm_mc.py` | Monte Carlo engine: topology comparison, scaling analysis, PRCC. No I/O. |
| `generate_swarm_figures.py` | Generates all 8 publication figures (`--fast` mode for CI). |

### Paper 03: Multi-Model AI Consensus

| File | Purpose |
|------|---------|
| `deliberation_analysis.py` | Parses 16 deliberation transcripts into structured datasets. |
| `generate_consensus_figures.py` | Generates all 8 publication figures (~1.2s). |

## Installation

```bash
cd publications/scripts
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Requires Python >= 3.10.

## Reproducing Paper Figures

```bash
source .venv/bin/activate

# Paper 01 — ISRU figures (~30s)
python generate_isru_figures.py

# Paper 02 — Swarm figures (--fast ~90s, full ~30min)
python generate_swarm_figures.py --fast

# Paper 03 — Consensus figures (~1.2s)
python generate_consensus_figures.py
```

Figures are written to `../drafts/<paper>/figures/`. Override with environment variables:

```bash
ISRU_FIG_DIR=./figs python generate_isru_figures.py
SWARM_FIG_DIR=./figs python generate_swarm_figures.py
```

All stochastic results use seed 42 for exact reproducibility.

## Running the Appendix Analysis

```bash
python extended_copula_sensitivity.py
```

## Tests

```bash
pytest                  # all tests
pytest -m "not slow"    # skip slow Monte Carlo convergence tests
pytest --cov            # with coverage
```

## License

MIT — see [LICENSE](LICENSE).
