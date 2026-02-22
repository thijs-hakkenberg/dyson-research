# ISRU Economic Crossover — Simulation Code

Companion code for the paper *"Economic Crossover Points for In-Situ Resource
Utilisation: A Parametric Cost Model with Monte Carlo Uncertainty
Quantification."*

## Modules

| File | Purpose |
|------|---------|
| `isru_model.py` | Pure cost model (Eqs. 1–9 + NPV extensions). No I/O. |
| `isru_mc.py` | Monte Carlo engine: sampling, loop, statistics, PRCC. No I/O. |
| `generate_isru_figures.py` | Generates all 6 publication figures + diagnostic tables. |
| `extended_copula_sensitivity.py` | Appendix: 6-D copula sensitivity analysis (AE1). |

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
python generate_isru_figures.py
```

Figures are written to `../drafts/01-isru-economic-crossover/figures/`.
Override the output directory with the `ISRU_FIG_DIR` environment variable:

```bash
ISRU_FIG_DIR=./my-figs python generate_isru_figures.py
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
