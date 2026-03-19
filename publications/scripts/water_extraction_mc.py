"""Monte Carlo engine for Paper 05: ISRU Water Extraction.

Version 2.0: Transport cost derived from physics. Adds rank-correlation
structure and Spearman sensitivity analysis.

Pure math module — no matplotlib, no prints.
"""

from __future__ import annotations

__version__ = "2.0.0"

from dataclasses import dataclass
from typing import Any
from numpy import (
    floating, array, clip, empty, percentile, mean, median,
    std as np_std, inf, zeros, argsort, corrcoef, abs as np_abs,
)
from numpy.random import Generator, default_rng
from numpy.typing import NDArray
from scipy.stats import spearmanr, rankdata

from water_extraction_model import (
    ASTEROID_BASELINE,
    LUNAR_BASELINE,
    PHOBOS_BASELINE,
    Params,
    npv_cost_per_kg,
    total_capital,
    npv_cost,
    payload_fraction,
    get_trip_time,
    transport_cost_per_kg_derived,
)

NDFloat = NDArray[floating[Any]]

# ---------------------------------------------------------------------------
# Parameter distributions (V2: physics-based transport)
# ---------------------------------------------------------------------------

ASTEROID_DISTRIBUTIONS: list[tuple[str, str, float, float]] = [
    ("water_fraction", "uniform", 0.05, 0.15),
    ("extraction_yield", "uniform", 0.50, 0.85),
    ("extraction_energy_kWh_per_kg", "uniform", 1.5, 4.0),
    ("K_extraction", "uniform", 3e9, 8e9),
    ("K_transport", "uniform", 7e9, 15e9),
    ("C_ops_per_kg", "uniform", 100, 400),
    ("delta_v_to_L4L5", "uniform", 3.0, 7.0),
    ("Isp", "uniform", 2000, 3000),
    ("vehicle_cost", "uniform", 300e6, 800e6),
    ("vehicle_lifetime_trips", "uniform", 10, 30),
    ("availability", "uniform", 0.70, 0.95),
]

LUNAR_DISTRIBUTIONS: list[tuple[str, str, float, float]] = [
    ("water_fraction", "uniform", 0.02, 0.10),
    ("extraction_yield", "uniform", 0.40, 0.75),
    ("extraction_energy_kWh_per_kg", "uniform", 2.5, 6.0),
    ("K_extraction", "uniform", 5e9, 12e9),
    ("K_transport", "uniform", 10e9, 25e9),
    ("K_surface_base", "uniform", 3e9, 10e9),
    ("C_ops_per_kg", "uniform", 200, 600),
    ("delta_v_to_L4L5", "uniform", 2.0, 3.5),
    ("Isp", "uniform", 420, 470),
    ("vehicle_cost", "uniform", 200e6, 500e6),
    ("vehicle_lifetime_trips", "uniform", 5, 15),
    ("availability", "uniform", 0.65, 0.90),
]


# ---------------------------------------------------------------------------
# Result dataclass
# ---------------------------------------------------------------------------

@dataclass
class WaterMCResult:
    """Results from a water extraction Monte Carlo run."""
    source_name: str
    n_samples: int
    npv_per_kg: NDFloat
    npv_total: NDFloat
    total_capital_arr: NDFloat
    param_samples: dict[str, NDFloat]  # for sensitivity analysis

    @property
    def median_per_kg(self) -> float:
        return float(median(self.npv_per_kg[self.npv_per_kg < inf]))

    @property
    def p10_per_kg(self) -> float:
        valid = self.npv_per_kg[self.npv_per_kg < inf]
        return float(percentile(valid, 10))

    @property
    def p90_per_kg(self) -> float:
        valid = self.npv_per_kg[self.npv_per_kg < inf]
        return float(percentile(valid, 90))

    @property
    def mean_per_kg(self) -> float:
        valid = self.npv_per_kg[self.npv_per_kg < inf]
        return float(mean(valid))


@dataclass
class SensitivityResult:
    """Spearman rank correlation for parameter sensitivity."""
    param_name: str
    rho: float
    p_value: float
    abs_rho: float


# ---------------------------------------------------------------------------
# Monte Carlo sampler
# ---------------------------------------------------------------------------

def sample_params(
    baseline: Params,
    distributions: list[tuple[str, str, float, float]],
    rng: Generator,
) -> Params:
    """Draw one random parameter set."""
    p = dict(baseline)
    for name, dist_type, a, b in distributions:
        if dist_type == "uniform":
            p[name] = float(rng.uniform(a, b))
        elif dist_type == "normal":
            p[name] = float(rng.normal(a, b))
        elif dist_type == "lognormal":
            p[name] = float(rng.lognormal(a, b))
    return p


def run_mc(
    source_name: str,
    baseline: Params,
    distributions: list[tuple[str, str, float, float]],
    n_samples: int = 10_000,
    seed: int = 42,
) -> WaterMCResult:
    """Run Monte Carlo simulation for a single water source."""
    rng = default_rng(seed)

    npv_kg = empty(n_samples)
    npv_tot = empty(n_samples)
    cap = empty(n_samples)
    param_samples: dict[str, list[float]] = {d[0]: [] for d in distributions}

    for i in range(n_samples):
        p = sample_params(baseline, distributions, rng)
        for name, _, _, _ in distributions:
            param_samples[name].append(p[name])
        try:
            npv_kg[i] = npv_cost_per_kg(p)
            npv_tot[i] = npv_cost(p)
            cap[i] = total_capital(p)
        except Exception:
            npv_kg[i] = inf
            npv_tot[i] = inf
            cap[i] = inf

    return WaterMCResult(
        source_name=source_name,
        n_samples=n_samples,
        npv_per_kg=npv_kg,
        npv_total=npv_tot,
        total_capital_arr=cap,
        param_samples={k: array(v) for k, v in param_samples.items()},
    )


def sensitivity_analysis(result: WaterMCResult) -> list[SensitivityResult]:
    """Compute Spearman rank correlations between parameters and NPV/kg."""
    valid = result.npv_per_kg < inf
    output = result.npv_per_kg[valid]

    results = []
    for name, samples in result.param_samples.items():
        param_valid = samples[valid]
        if len(param_valid) < 10:
            continue
        rho, pval = spearmanr(param_valid, output)
        results.append(SensitivityResult(
            param_name=name,
            rho=float(rho),
            p_value=float(pval),
            abs_rho=float(abs(rho)),
        ))

    results.sort(key=lambda x: x.abs_rho, reverse=True)
    return results


def run_all_sources(
    n_samples: int = 10_000,
    seed: int = 42,
) -> dict[str, WaterMCResult]:
    """Run MC for asteroid and lunar sources."""
    return {
        "C-type NEA": run_mc(
            "C-type NEA", ASTEROID_BASELINE, ASTEROID_DISTRIBUTIONS,
            n_samples=n_samples, seed=seed,
        ),
        "Lunar polar ice": run_mc(
            "Lunar polar ice", LUNAR_BASELINE, LUNAR_DISTRIBUTIONS,
            n_samples=n_samples, seed=seed + 1,
        ),
    }


def probability_asteroid_cheaper(
    n_samples: int = 10_000,
    seed: int = 42,
) -> float:
    """Compute probability that asteroid source is cheaper than lunar."""
    rng = default_rng(seed)
    count_cheaper = 0
    for i in range(n_samples):
        p_ast = sample_params(ASTEROID_BASELINE, ASTEROID_DISTRIBUTIONS, rng)
        p_lun = sample_params(LUNAR_BASELINE, LUNAR_DISTRIBUTIONS, rng)
        try:
            cost_ast = npv_cost_per_kg(p_ast)
            cost_lun = npv_cost_per_kg(p_lun)
            if cost_ast < cost_lun:
                count_cheaper += 1
        except Exception:
            pass
    return count_cheaper / n_samples
