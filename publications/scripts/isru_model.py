"""Pure cost model for the ISRU Economic Crossover paper.

Implements Equations 1-9 (plus NPV extensions). No matplotlib, no prints —
all functions are pure math suitable for testing and reuse.
"""

from __future__ import annotations
from typing import Any
from numpy import floating, log, maximum, asarray, arange, ones_like, exp as np_exp, where as np_where, cumsum, log1p
from numpy.typing import NDArray

# ---------------------------------------------------------------------------
# Type aliases
# ---------------------------------------------------------------------------
NDFloat = NDArray[floating[Any]]
Params = dict[str, Any]

# ---------------------------------------------------------------------------
# Baseline parameters (Table 1 in paper)
# ---------------------------------------------------------------------------
BASELINE: Params = {
    "m": 1850,              # unit mass (kg)
    "p_launch": 1000,       # launch cost ($/kg)
    "K": 50e9,              # ISRU capital ($)
    "C_mfg1": 75e6,         # first-unit Earth manufacturing cost ($)
    "C_ops1": 5e6,          # first-unit ISRU ops cost ($)
    "LR_E": 0.85,           # Earth learning rate
    "LR_I": 0.90,           # ISRU learning rate
    "t0": 5,                # ramp-up midpoint (years)
    "k_ramp": 2.0,          # S-curve steepness
    "N_total": 10000,       # amortization horizon
    "prod_rate": 500,       # units/year at full capacity
    "C_floor": 0.5e6,       # ISRU ops cost floor ($)
    "r": 0.05,              # discount rate (real)
    "b_L": None,            # launch learning exponent (None = no learning)
    "p_fuel": 200,          # fuel component of launch cost ($/kg)
    "p_ops_launch": 800,    # ops component of launch cost ($/kg)
    "alpha": 1.0,           # D5: mass penalty factor for ISRU units
    "p_transport": 100,     # D6: ISRU-to-orbit transport cost ($/kg)
}

# ---------------------------------------------------------------------------
# Parameter bounds for clamping
# ---------------------------------------------------------------------------
PARAM_BOUNDS: dict[str, tuple[float | None, float | None]] = {
    "r": (0.0, None),
    "alpha": (1.0, None),
    "p_transport": (0.0, None),
    "LR_E": (0.5, 1.0),
    "LR_I": (0.5, 1.0),
    "K": (0.0, None),
    "C_ops1": (0.0, None),
    "C_mfg1": (0.0, None),
    "p_launch": (0.0, None),
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def significance_stars(pval: float) -> str:
    """Return significance stars for a p-value."""
    if pval < 0.001:
        return "***"
    if pval < 0.01:
        return "**"
    if pval < 0.05:
        return "*"
    return ""


def clamp_param(param: str, value: float) -> float:
    """Clamp a parameter value to its valid bounds."""
    bounds = PARAM_BOUNDS.get(param)
    if bounds is None:
        return value
    lo, hi = bounds
    if lo is not None:
        value = max(lo, value)
    if hi is not None:
        value = min(hi, value)
    return value


# ---------------------------------------------------------------------------
# Cost model (Equations 1-9 plus NPV extensions)
# ---------------------------------------------------------------------------
def learning_exponent(lr: float) -> float:
    """Wright learning curve exponent: b = ln(LR) / ln(2)."""
    return log(lr) / log(2)


def s_curve(t: float | NDFloat, t0: float, k: float = 2.0) -> float | NDFloat:
    """Logistic ramp-up function S(t) = 1 / (1 + exp(-k*(t - t0)))."""
    return 1.0 / (1.0 + np_exp(-k * (t - t0)))


def _cumulative_production(
    t: float | NDFloat, prod_rate: float, t0: float, k: float
) -> NDFloat:
    """Cumulative production N(t) by integrating n_dot(t) = prod_rate * S(t).

    The integral of the logistic S(t) has closed form:
      N(t) = (prod_rate / k) * [ln(1 + exp(k*(t - t0))) - ln(2)]
    """
    t = asarray(t, dtype=float)
    # Use log-sum-exp trick for numerical stability
    arg = k * (t - t0)
    # ln(1 + exp(x)) = x + ln(1 + exp(-x)) for large x (avoids overflow)
    log1p_exp = np_where(arg > 20, arg, log1p(np_exp(arg)))
    return (prod_rate / k) * (log1p_exp - log(2))


def unit_to_time(
    n: float | NDFloat,
    prod_rate: float = 500,
    t0: float = 5,
    k: float = 2.0,
) -> NDFloat:
    """Map unit number to calendar time by inverting N(t).

    Closed-form inverse of N(t) = (prod_rate/k) * [ln(1+exp(k*(t-t0))) - ln(2)]:
      t(n) = t0 + (1/k) * ln(2*exp(n*k/prod_rate) - 1)

    For large n*k/prod_rate (>30), uses asymptotic form to avoid overflow:
      t(n) ~ t0 + n/prod_rate + ln(2)/k

    Fully vectorized.
    """
    n = asarray(n, dtype=float)
    x = n * k / prod_rate  # dimensionless argument

    result = np_where(
        x < 30,
        t0 + (1.0 / k) * log(maximum(2.0 * np_exp(x) - 1.0, 1e-300)),
        t0 + n / prod_rate + log(2.0) / k,
    )
    return result


def earth_unit_cost(n: float | NDFloat, params: Params) -> NDFloat:
    """Eq 2-4: Earth per-unit cost = manufacturing learning + launch."""
    n = asarray(n, dtype=float)
    b_E = learning_exponent(params["LR_E"])
    c_mfg = params["C_mfg1"] * n ** b_E

    # Launch cost: optionally with learning on ops component
    b_L = params.get("b_L", None)
    if b_L is not None:
        p_fuel = params.get("p_fuel", 200)
        p_ops = params.get("p_ops_launch", 800)
        c_launch = params["m"] * (p_fuel + p_ops * n ** b_L)
    else:
        c_launch = params["m"] * params["p_launch"]

    return c_mfg + c_launch


def earth_unit_cost_launch_learning(
    n: float | NDFloat, params: Params
) -> NDFloat:
    """Launch cost with two-component learning model.

    C_L(n) = m * [p_fuel + p_ops * n^b_L]
    where b_L = ln(LR_L) / ln(2), and only the ops component learns.
    """
    n = asarray(n, dtype=float)
    p_fuel = params.get("p_fuel", 200)
    p_ops = params.get("p_ops_launch", 800)
    lr_launch = params.get("LR_launch", 0.97)
    b_L = learning_exponent(lr_launch)
    return params["m"] * (p_fuel + p_ops * n ** b_L)


def isru_ops_cost(n: float | NDFloat, params: Params) -> NDFloat:
    """Operational cost only (no amortized capital).

    Ramp-up effect is through production schedule timing (unit_to_time
    integrates S(t)). Mass penalty alpha multiplies ops cost.
    Transport cost added as m * p_transport * alpha.
    """
    n = asarray(n, dtype=float)
    b_i = learning_exponent(params["LR_I"])
    alpha = params.get("alpha", 1.0)
    c_floor = params.get("C_floor", 0)

    # Learning curve ops cost
    c_ops = alpha * (c_floor + (params["C_ops1"] - c_floor) * n ** b_i)

    # Transport cost
    p_transport = params.get("p_transport", 0)
    if p_transport > 0:
        c_transport = params["m"] * p_transport * alpha
        c_ops = c_ops + c_transport

    return c_ops


def isru_unit_cost(n: float | NDFloat, params: Params) -> NDFloat:
    """ISRU per-unit cost = amortized capital + ops (for display)."""
    c_capital = params["K"] / params["N_total"]
    return c_capital + isru_ops_cost(n, params)


def cumulative_cost(
    unit_cost_fn: Any, n_max: int, params: Params
) -> tuple[NDFloat, NDFloat, NDFloat]:
    """Compute cumulative cost for units 1..N_max."""
    ns = arange(1, n_max + 1, dtype=float)
    unit_costs = unit_cost_fn(ns, params)
    cum = cumsum(unit_costs)
    return ns, unit_costs, cum


def cumulative_isru(
    n_max: int, params: Params
) -> tuple[NDFloat, NDFloat, NDFloat]:
    """Eq 9: ISRU cumulative = K + sum of ops costs."""
    ns = arange(1, n_max + 1, dtype=float)
    ops_costs = isru_ops_cost(ns, params)
    cum = params["K"] + cumsum(ops_costs)
    # Per-unit costs include amortized capital (for display)
    unit_costs = params["K"] / params["N_total"] + ops_costs
    return ns, unit_costs, cum


def earth_delivery_time(ns: float | NDFloat, prod_rate: float = 500) -> NDFloat:
    """Earth delivery time — constant rate from t=0 (no ramp-up delay).

    Earth manufacturing can begin immediately, so t_{n,E} = n / prod_rate.
    """
    return asarray(ns, dtype=float) / prod_rate


def earth_delivery_time_ramped(
    ns: float | NDFloat,
    prod_rate: float = 500,
    t0_earth: float = 1.0,
    k_earth: float = 2.0,
) -> NDFloat:
    """Earth delivery time with logistic ramp-up (robustness test).

    Like the ISRU schedule but with a shorter ramp-up delay.
    Uses the same integrated-logistic inverse as unit_to_time.
    """
    return unit_to_time(asarray(ns, dtype=float), prod_rate, t0_earth, k_earth)


def find_crossover(
    params: Params,
    n_max: int = 20000,
    *,
    discount: bool = False,
    phased_k_years: int | None = None,
    earth_ramp: tuple[float, float] | None = None,
) -> int:
    """Find smallest N where ISRU cumulative <= Earth cumulative.

    Parameters
    ----------
    params : dict
        Model parameters.
    n_max : int
        Maximum units to search.
    discount : bool
        If True, use NPV discounting with pathway-specific timing.
    phased_k_years : int or None
        If set, spread capital K over this many annual tranches (requires discount=True).
    earth_ramp : tuple(t0_earth, k_earth) or None
        If set, use logistic ramp-up for Earth delivery schedule instead of
        instant-start. Tuple is (midpoint_years, steepness).
    """
    r = params.get("r", 0.0) if discount else 0.0

    # If discount requested but r==0, fall back to undiscounted
    if r == 0.0:
        discount = False
        phased_k_years = None

    ns = arange(1, n_max + 1, dtype=float)
    prod_rate = params.get("prod_rate", 500)
    k_ramp = params.get("k_ramp", 2.0)

    # Earth side
    earth_units = earth_unit_cost(ns, params)
    if discount:
        if earth_ramp is not None:
            t0_e, k_e = earth_ramp
            t_n_earth = earth_delivery_time_ramped(ns, prod_rate, t0_e, k_e)
        else:
            t_n_earth = earth_delivery_time(ns, prod_rate)
        discount_earth = (1.0 + r) ** (-t_n_earth)
        earth_cum = cumsum(earth_units * discount_earth)
    else:
        earth_cum = cumsum(earth_units)

    # ISRU side — ops
    ops = isru_ops_cost(ns, params)
    if discount:
        t_n_isru = unit_to_time(ns, prod_rate, params["t0"], k_ramp)
        discount_isru = (1.0 + r) ** (-t_n_isru)
        isru_ops_cum = cumsum(ops * discount_isru)
    else:
        isru_ops_cum = cumsum(ops)

    # Capital
    K = params["K"]
    if phased_k_years is not None and discount:
        tranche = K / phased_k_years
        K_eff = sum(tranche / (1.0 + r) ** y for y in range(phased_k_years))
    else:
        K_eff = K

    isru_cum = K_eff + isru_ops_cum

    # Find crossover
    diff = isru_cum - earth_cum
    crossings = np_where(diff <= 0)[0]
    if len(crossings) > 0:
        return int(ns[crossings[0]])
    return n_max


# Backward-compat shims
def find_crossover_npv(params: Params, N_max: int = 20000) -> int:
    """Find NPV crossover (backward-compatible wrapper)."""
    return find_crossover(params, N_max, discount=True)


def find_crossover_npv_phased(
    params: Params, N_max: int = 20000, K_years: int = 5
) -> int:
    """Find NPV crossover with phased capital (backward-compatible wrapper)."""
    return find_crossover(params, N_max, discount=True, phased_k_years=K_years)


def cumulative_npv(
    n_max: int, params: Params
) -> tuple[NDFloat, NDFloat, NDFloat]:
    """Compute discounted cumulative costs for both pathways."""
    r = params.get("r", 0.0)
    ns = arange(1, n_max + 1, dtype=float)
    prod_rate = params.get("prod_rate", 500)
    k_ramp = params.get("k_ramp", 2.0)

    t_n_earth = earth_delivery_time(ns, prod_rate)
    t_n_isru = unit_to_time(ns, prod_rate, params["t0"], k_ramp)

    discount_earth = (1.0 + r) ** (-t_n_earth) if r > 0 else ones_like(ns)
    discount_isru = (1.0 + r) ** (-t_n_isru) if r > 0 else ones_like(ns)

    earth_units = earth_unit_cost(ns, params)
    earth_cum = cumsum(earth_units * discount_earth)

    ops = isru_ops_cost(ns, params)
    isru_cum = params["K"] + cumsum(ops * discount_isru)

    return ns, earth_cum, isru_cum
