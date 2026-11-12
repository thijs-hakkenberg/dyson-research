"""
Phase 0 cost confidence (rq-0-84): do the bom-0-17 contingency rates reach the confidence they
are meant to, and how likely is 0A within the D-01 assumption A4 ($3.5–16B)?

Inputs are the consensus envelopes in src/lib/data/phase-0-bom.json (built from
reconciliation/phase-0/bom-numbers.yaml). Method:
  - Each item and sub-phase is a lognormal whose envelope ends are its P10 and P90
    (sensitivity: P5/P95). Envelopes with a zero low end are uniform on [0, max]; a
    conditional item (bom-0-6 water pilot) is flown with probability p_conditional.
  - Items are tied by a Gaussian copula with one common correlation ρ (0, 0.3, 0.5).
  - The funded figure is the planning point (consensus value or midpoint) × (1 + rate),
    which is how bom-0-17 is computed. Its confidence is P(total ≤ funded).
  - Cost growth (optional): the envelopes are the spread between model estimates, not
    the overrun history of first-of-kind space hardware. `growth` multiplies each
    development or hardware line by a lognormal growth factor (median, P90) on the same
    copula; commodity and service lines (launch, propellant, comms, ops, organisation) are
    left alone. NASA science missions have averaged roughly 30–50% growth over their
    confirmation estimates (GAO, Assessments of Major Projects), and estimates made at
    concept stage for new technology grow more; (1.3, 2.0) and (1.5, 2.5) bracket that.
  - 0A duration (CI-27): KDP-0B falls between month 72 and 180 (D-02). Lines priced per year
    (ops bom-0-10, organisation bom-0-7, comms bom-0-9) are rescaled from the duration their
    consensus assumed (ASSUMED_0A_YEARS) to the drawn duration; a share of NRE (bom-0-11) can
    be level-of-effort and rescaled too.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass

import numpy as np
from scipy.stats import norm

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
# In the web repo the BOM is the generated site data; the research archive (dyson-research)
# carries a snapshot of the same file under publications/data/phase0-bom/.
_BOM_PATHS = [
    os.path.join(ROOT, 'src', 'lib', 'data', 'phase-0-bom.json'),
    os.path.join(ROOT, 'publications', 'data', 'phase0-bom', 'phase-0-bom.json'),
]
BOM_JSON = next((p for p in _BOM_PATHS if os.path.exists(p)), _BOM_PATHS[0])

Z90 = norm.ppf(0.9)
Z95 = norm.ppf(0.95)
# 0A length the run-rate lines were priced on (bom-0-10 consensus: 0A about 4–5.5 yr)
ASSUMED_0A_YEARS = 5.0
RUN_RATE_0A = ('bom-0-7', 'bom-0-9', 'bom-0-10')


def load_bom(path: str = BOM_JSON) -> dict:
    return json.load(open(path))


@dataclass
class Settings:
    rho: float = 0.3
    tail: str = 'P10/P90'  # or 'P5/P95'
    p_conditional: float = 0.5
    n: int = 200_000
    seed: int = 7
    duration_years: tuple | None = None  # (lo, hi) uniform 0A length; None = as priced
    nre_level_of_effort: float = 0.0
    growth: tuple | None = None  # (median, P90) cost-growth factor on development/hardware lines


# Lines whose cost is mostly a market price or a run rate, not new development
NO_GROWTH = ('bom-0-7', 'bom-0-8', 'bom-0-9', 'bom-0-10', 'bom-0-16')


def _marginal(u: np.ndarray, env: dict, z: float, p_cond: float) -> np.ndarray:
    lo, hi = env['min'], env['max']
    if hi <= 0:
        return np.zeros_like(u)
    if env.get('conditional'):
        ie = env['ifExercised']
        flown = u < p_cond
        u2 = np.where(flown, u / p_cond, 0.5)
        return np.where(flown, _lognormal(u2, ie['min'], ie['max'], z), 0.0)
    if lo <= 0:
        return u * hi
    return _lognormal(u, lo, hi, z)


def _lognormal(u, lo, hi, z):
    mu = 0.5 * (np.log(lo) + np.log(hi))
    sigma = (np.log(hi) - np.log(lo)) / (2 * z)
    return np.exp(mu + sigma * norm.ppf(np.clip(u, 1e-12, 1 - 1e-12)))


def sample_lines(bom: dict, s: Settings, rng: np.random.Generator | None = None) -> dict:
    """Per-item cost draws: {bomId: (0A array, 0B array)}, contingency (bom-0-17) excluded."""
    rng = rng or np.random.default_rng(s.seed)
    z = Z90 if s.tail == 'P10/P90' else Z95
    items = [i for i in bom['items'] if i['bomId'] != 'bom-0-17']
    k = 3 * len(items)
    common = rng.standard_normal(s.n)
    idio = rng.standard_normal((s.n, k))
    u = norm.cdf(np.sqrt(s.rho) * common[:, None] + np.sqrt(1 - s.rho) * idio)
    years = rng.uniform(*s.duration_years, s.n) if s.duration_years else None
    out = {}
    for j, it in enumerate(items):
        xa = _marginal(u[:, 3 * j], it['a'], z, s.p_conditional)
        xb = _marginal(u[:, 3 * j + 1], it['b'], z, s.p_conditional)
        if s.growth and it['bomId'] not in NO_GROWTH:
            med, p90 = s.growth
            q = norm.ppf(np.clip(u[:, 3 * j + 2], 1e-12, 1 - 1e-12))
            g = np.exp(np.log(med) + (np.log(p90) - np.log(med)) / Z90 * q)
            xa, xb = xa * g, xb * g
        if years is not None:
            if it['bomId'] in RUN_RATE_0A:
                xa = xa * years / ASSUMED_0A_YEARS
            elif it['bomId'] == 'bom-0-11' and s.nre_level_of_effort:
                f = s.nre_level_of_effort
                xa = xa * ((1 - f) + f * years / ASSUMED_0A_YEARS)
        out[it['bomId']] = (xa, xb)
    return out


def simulate(bom: dict, s: Settings = Settings()) -> dict:
    lines = sample_lines(bom, s)
    a = sum(x[0] for x in lines.values())
    b = sum(x[1] for x in lines.values())
    c = bom['totals']['contingency']
    base = bom['totals']['base']
    funded_a = base['a']['point'] * (1 + c['a']['ratePoint'])
    funded_b = base['b']['point'] * (1 + c['b']['ratePoint'])

    def stats(x, funded):
        return {
            'P10': float(np.quantile(x, 0.1)),
            'P50': float(np.quantile(x, 0.5)),
            'P80': float(np.quantile(x, 0.8)),
            'P90': float(np.quantile(x, 0.9)),
            'mean': float(x.mean()),
            'funded': float(funded),
            'confidence_of_funded': float((x <= funded).mean()),
        }

    ra = stats(a, funded_a)
    ra['rate_needed_for_P80'] = float(np.quantile(a, 0.8) / base['a']['point'] - 1)
    ra['P(<=16B)'] = float((a <= 16e9).mean())
    rb = stats(b, funded_b)
    rb['rate_needed_for_P80'] = float(np.quantile(b, 0.8) / base['b']['point'] - 1)
    return {'0A': ra, '0B': rb}
