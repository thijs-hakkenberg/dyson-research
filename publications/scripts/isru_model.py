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
    "b_L": log(0.97) / log(2),  # launch learning exponent (LR_L=0.97 baseline)
    "p_fuel": 200,          # fuel component of launch cost ($/kg)
    "p_ops_launch": 800,    # ops component of launch cost ($/kg)
    "alpha": 1.0,           # D5: mass penalty factor for ISRU units
    "p_transport": 100,     # D6: ISRU-to-orbit transport cost ($/kg)
    "vitamin_frac": 0.0,    # G11: fraction of unit that must be Earth-sourced
    "c_vitamin_kg": 10000,  # M1: vitamin component mfg cost ($/kg, electronics ~$10k/kg)
    "launches_per_unit": 1.0,  # M2: launches per unit for launch learning index
    "K_maint_frac": 0.0,   # M3: fraction of K spent on maintenance per interval
    "K_maint_interval": 5,  # M3: years between maintenance overhauls
    "C_mfg_floor": 0,      # N1: Earth mfg cost floor ($/unit, 0 = no floor)
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


def unit_to_time_piecewise(
    n: float | NDFloat,
    prod_rate: float = 500,
    t0: float = 5,
    k: float = 2.0,
    t_construction: float | None = None,
) -> NDFloat:
    """Map unit number to calendar time with explicit construction delay.

    For t < t_c, production rate is zero (construction phase).
    For t >= t_c, logistic ramp-up centered at t_c + delta.
    Default t_c = t0 - 1 (construction ends 1yr before logistic midpoint).

    This is a sensitivity variant of unit_to_time(); at large t the two
    converge because the logistic asymptotes to the same linear regime.
    """
    if t_construction is None:
        t_construction = t0 - 1.0

    n = asarray(n, dtype=float)
    # Shift the logistic midpoint to start after construction
    # The effective midpoint is t_construction + (t0 - t_construction) = t0
    # So for default t_c = t0-1, the midpoint is still t0.
    # But the piecewise constraint means N(t<t_c) = 0.
    # We compute the baseline t(n) and clamp: t_pw = max(t(n), t_c).
    t_baseline = unit_to_time(n, prod_rate, t0, k)
    return maximum(t_baseline, t_construction)


def find_crossover_mfg_lead(
    params: Params,
    n_max: int = 20000,
    *,
    tau_mfg: float = 0.5,
) -> int:
    """Find NPV crossover with manufacturing lead-time adjustment.

    Earth manufacturing cost is discounted at t_{n,E} - tau_mfg (paid earlier),
    while Earth launch cost is discounted at t_{n,E} (at delivery).
    This tests the sensitivity of the pay-at-delivery simplification.
    """
    r = params.get("r", 0.05)
    ns = arange(1, n_max + 1, dtype=float)
    prod_rate = params.get("prod_rate", 500)
    k_ramp = params.get("k_ramp", 2.0)

    # Earth side — split mfg and launch timing
    b_E = learning_exponent(params["LR_E"])
    c_mfg = params["C_mfg1"] * ns ** b_E

    # N1: Earth manufacturing cost floor
    C_mfg_floor = params.get("C_mfg_floor", 0)
    if C_mfg_floor > 0:
        c_mfg = maximum(c_mfg, C_mfg_floor)

    # Launch cost: optionally with learning on ops component
    b_L = params.get("b_L", None)
    if b_L is not None:
        p_fuel = params.get("p_fuel", 200)
        p_ops = params.get("p_ops_launch", 800)
        launches_per_unit = params.get("launches_per_unit", 1.0)
        n_launches = ns * launches_per_unit
        c_launch = params["m"] * (p_fuel + p_ops * n_launches ** b_L)
    else:
        c_launch = params["m"] * params["p_launch"] * ones_like(ns)

    t_n_earth = earth_delivery_time(ns, prod_rate)
    t_mfg = maximum(t_n_earth - tau_mfg, 0.0)  # mfg cost paid earlier

    discount_mfg = (1.0 + r) ** (-t_mfg)
    discount_launch = (1.0 + r) ** (-t_n_earth)
    earth_cum = cumsum(c_mfg * discount_mfg + c_launch * discount_launch)

    # ISRU side — unchanged
    ops = isru_ops_cost(ns, params)
    t_n_isru = unit_to_time(ns, prod_rate, params["t0"], k_ramp)
    discount_isru = (1.0 + r) ** (-t_n_isru)
    isru_ops_cum = cumsum(ops * discount_isru)
    isru_cum = params["K"] + isru_ops_cum

    diff = isru_cum - earth_cum
    crossings = np_where(diff <= 0)[0]
    if len(crossings) > 0:
        return int(ns[crossings[0]])
    return n_max


def earth_unit_cost(n: float | NDFloat, params: Params) -> NDFloat:
    """Eq 2-4: Earth per-unit cost = manufacturing learning + launch."""
    n = asarray(n, dtype=float)
    b_E = learning_exponent(params["LR_E"])
    c_mfg = params["C_mfg1"] * n ** b_E

    # N1: Earth manufacturing cost floor
    C_mfg_floor = params.get("C_mfg_floor", 0)
    if C_mfg_floor > 0:
        c_mfg = maximum(c_mfg, C_mfg_floor)

    # Launch cost: optionally with learning on ops component
    # M2: launches_per_unit re-indexes learning to cumulative launches
    b_L = params.get("b_L", None)
    if b_L is not None:
        p_fuel = params.get("p_fuel", 200)
        p_ops = params.get("p_ops_launch", 800)
        launches_per_unit = params.get("launches_per_unit", 1.0)
        n_launches = n * launches_per_unit
        c_launch = params["m"] * (p_fuel + p_ops * n_launches ** b_L)
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
    Vitamin fraction adds Earth-sourced component cost.
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

    # Vitamin fraction: Earth-sourced components that ISRU cannot produce.
    # Two-part model (M1): ISRU processes (1-fv) of the unit; the vitamin
    # portion must be launched from Earth and has its own mfg cost per kg.
    # c_vitamin = fv * m * (p_launch_effective + c_vitamin_kg)
    vitamin_frac = params.get("vitamin_frac", 0.0)
    if vitamin_frac > 0:
        c_vitamin_kg = params.get("c_vitamin_kg", 10000)
        # Effective launch cost for vitamins (with learning if active)
        b_L = params.get("b_L", None)
        if b_L is not None:
            p_fuel = params.get("p_fuel", 200)
            p_ops = params.get("p_ops_launch", 800)
            launches_per_unit = params.get("launches_per_unit", 1.0)
            n_launches = n * launches_per_unit
            p_launch_eff = p_fuel + p_ops * n_launches ** b_L
        else:
            p_launch_eff = params.get("p_launch", 1000)
        c_vitamin_launch = vitamin_frac * params["m"] * p_launch_eff
        c_vitamin_mfg = vitamin_frac * params["m"] * c_vitamin_kg
        c_ops = (1.0 - vitamin_frac) * c_ops + c_vitamin_launch + c_vitamin_mfg

    return c_ops


def isru_ops_cost_rate_dependent(
    n: float | NDFloat, params: Params, *, rate_threshold: float = 0.2
) -> NDFloat:
    """ISRU ops cost with rate-dependent learning (organizational forgetting).

    When the instantaneous production rate S(t_n) < rate_threshold * n_max,
    learning is frozen: the cost of units produced during slow periods equals
    the cost of the last unit produced above the threshold.

    This approximates organizational forgetting during low-activity periods.
    """
    n = asarray(n, dtype=float)
    b_i = learning_exponent(params["LR_I"])
    alpha = params.get("alpha", 1.0)
    c_floor = params.get("C_floor", 0)
    prod_rate = params.get("prod_rate", 500)
    t0 = params["t0"]
    k_ramp = params.get("k_ramp", 2.0)

    # Compute time and instantaneous rate for each unit
    t_n = unit_to_time(n, prod_rate, t0, k_ramp)
    s_t = s_curve(t_n, t0, k_ramp)
    above_threshold = s_t >= rate_threshold

    # Base learning curve cost (without rate-dependent freezing)
    c_learn = c_floor + (params["C_ops1"] - c_floor) * n ** b_i

    # For units below threshold, freeze at the cost of the last above-threshold unit
    # Find the effective unit number for learning (frozen during slow periods)
    # Use cumulative max of (n * above_threshold) to carry forward last active n
    effective_n = n.copy()
    last_active = 0.0
    for i in range(len(n)):
        if above_threshold[i]:
            last_active = n[i]
        elif last_active > 0:
            effective_n[i] = last_active
    c_learn_rd = c_floor + (params["C_ops1"] - c_floor) * effective_n ** b_i

    c_ops = alpha * c_learn_rd

    # Transport cost
    p_transport = params.get("p_transport", 0)
    if p_transport > 0:
        c_ops = c_ops + params["m"] * p_transport * alpha

    # Vitamin fraction (same two-part model as isru_ops_cost)
    vitamin_frac = params.get("vitamin_frac", 0.0)
    if vitamin_frac > 0:
        c_vitamin_kg = params.get("c_vitamin_kg", 10000)
        b_L = params.get("b_L", None)
        if b_L is not None:
            p_fuel = params.get("p_fuel", 200)
            p_ops = params.get("p_ops_launch", 800)
            launches_per_unit = params.get("launches_per_unit", 1.0)
            n_launches = n * launches_per_unit
            p_launch_eff = p_fuel + p_ops * n_launches ** b_L
        else:
            p_launch_eff = params.get("p_launch", 1000)
        c_vitamin_launch = vitamin_frac * params["m"] * p_launch_eff
        c_vitamin_mfg = vitamin_frac * params["m"] * c_vitamin_kg
        c_ops = (1.0 - vitamin_frac) * c_ops + c_vitamin_launch + c_vitamin_mfg

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

    # M3: Ongoing capital maintenance — periodic injection of K_maint_frac * K
    K_maint_frac = params.get("K_maint_frac", 0.0)
    maint_cost = 0.0
    if K_maint_frac > 0 and discount:
        K_maint_interval = params.get("K_maint_interval", 5)
        t_horizon = float(unit_to_time(n_max, prod_rate, params["t0"], k_ramp))
        maint_cost = sum(
            (K * K_maint_frac) / (1.0 + r) ** t
            for t in range(K_maint_interval, int(t_horizon) + 1, K_maint_interval)
        )

    isru_cum = K_eff + maint_cost + isru_ops_cum

    # Find crossover
    diff = isru_cum - earth_cum
    crossings = np_where(diff <= 0)[0]
    if len(crossings) > 0:
        return int(ns[crossings[0]])
    return n_max


def find_crossover_rate_dependent(
    params: Params,
    n_max: int = 20000,
    *,
    rate_threshold: float = 0.2,
) -> int:
    """Find NPV crossover using rate-dependent ISRU learning."""
    r = params.get("r", 0.05)
    ns = arange(1, n_max + 1, dtype=float)
    prod_rate = params.get("prod_rate", 500)
    k_ramp = params.get("k_ramp", 2.0)

    # Earth side
    earth_units = earth_unit_cost(ns, params)
    t_n_earth = earth_delivery_time(ns, prod_rate)
    discount_earth = (1.0 + r) ** (-t_n_earth)
    earth_cum = cumsum(earth_units * discount_earth)

    # ISRU side with rate-dependent ops
    ops = isru_ops_cost_rate_dependent(ns, params, rate_threshold=rate_threshold)
    t_n_isru = unit_to_time(ns, prod_rate, params["t0"], k_ramp)
    discount_isru = (1.0 + r) ** (-t_n_isru)
    isru_ops_cum = cumsum(ops * discount_isru)

    isru_cum = params["K"] + isru_ops_cum
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
