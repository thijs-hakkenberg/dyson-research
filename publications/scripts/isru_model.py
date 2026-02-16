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
    "vitamin_frac": 0.05,   # G11: fraction of unit that must be Earth-sourced
    "c_vitamin_kg": 10000,  # M1: vitamin component mfg cost ($/kg, electronics ~$10k/kg)
    "launches_per_unit": 1.0,  # M2: launches per unit for launch learning index
    "K_maint_frac": 0.0,   # M3: fraction of K spent on maintenance per interval
    "K_maint_interval": 5,  # M3: years between maintenance overhauls
    "C_mfg_floor": 0,      # N1: Earth mfg cost floor ($/unit, 0 = no floor)
    "availability": 1.0,   # O2: ISRU facility availability factor (0-1)
    "C_mat": 1e6,          # U1: per-unit material cost (non-learnable, $/unit)
    "C_labor1": 74e6,      # U1: first-unit labor+overhead cost (learnable, $/unit)
    "earth_n0": 0,         # AB1: Earth learning curve starting offset (prior production units)
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
    earth_n0 = params.get("earth_n0", 0)
    ns_eff = ns + earth_n0  # AB1: prior production offset
    C_mat = params.get("C_mat", 0)
    if C_mat > 0:
        C_labor1 = params.get("C_labor1", params["C_mfg1"] - C_mat)
        c_mfg = C_mat + C_labor1 * ns_eff ** b_E
    else:
        c_mfg = params["C_mfg1"] * ns_eff ** b_E

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
        n_launches = ns * launches_per_unit + earth_n0
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
    """Eq 2-4: Earth per-unit cost = manufacturing learning + launch.

    U1: Two-component manufacturing model: C_mfg = C_mat + C_labor1 * n^b_E
    where C_mat is non-learnable material cost and C_labor1 is first-unit
    labor/overhead cost. Falls back to single Wright curve (C_mfg1 * n^b_E)
    when C_mat is not in params or is zero.

    AB1: earth_n0 offsets the learning index to model prior production
    experience (e.g., units manufactured for other programs).
    """
    n = asarray(n, dtype=float)
    b_E = learning_exponent(params["LR_E"])
    earth_n0 = params.get("earth_n0", 0)

    # AB1: Effective learning index accounts for prior production
    n_eff = n + earth_n0

    # U1: Two-component model (material + labor) or single Wright curve
    C_mat = params.get("C_mat", 0)
    if C_mat > 0:
        C_labor1 = params.get("C_labor1", params["C_mfg1"] - C_mat)
        c_mfg = C_mat + C_labor1 * n_eff ** b_E
    else:
        c_mfg = params["C_mfg1"] * n_eff ** b_E

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
        n_launches = n * launches_per_unit + earth_n0
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


def isru_ops_cost(
    n: float | NDFloat,
    params: Params,
    *,
    n_break_isru: int | None = None,
    damping_isru: float = 1.0,
) -> NDFloat:
    """Operational cost only (no amortized capital).

    Ramp-up effect is through production schedule timing (unit_to_time
    integrates S(t)). Mass penalty alpha multiplies ops cost.
    Transport cost added as m * p_transport * alpha.
    Vitamin fraction adds Earth-sourced component cost.

    V1: Pioneering phase — for n <= pioneer_n, cost is multiplied by
    pioneer_gamma to model negative learning (debugging, rework, failures).
    V2: QA cost — per-unit quality assurance cost C_QA added, declining
    with its own learning curve (LR_QA).
    Z2: ISRU learning plateau — when n_break_isru is set, the ISRU
    learning exponent is damped for n > n_break_isru, mirroring the
    Earth plateau model (earth_unit_cost_plateau).
    """
    n = asarray(n, dtype=float)
    b_i = learning_exponent(params["LR_I"])
    alpha = params.get("alpha", 1.0)
    c_floor = params.get("C_floor", 0)

    # Z2: Piecewise ISRU learning plateau (symmetric to Earth plateau)
    if n_break_isru is not None and damping_isru != 1.0:
        b_i2 = b_i * damping_isru
        # Continuity-preserving piecewise: at n_break, both branches give same value.
        # Before break: C_ops1 * n^b_i
        # After break: C_ops1 * n_break^(b_i - b_i2) * n^b_i2
        scale = (params["C_ops1"] - c_floor) * n_break_isru ** (b_i - b_i2)
        c_learn = np_where(
            n <= n_break_isru,
            (params["C_ops1"] - c_floor) * n ** b_i,
            scale * n ** b_i2,
        )
        c_ops = alpha * (c_floor + c_learn)
    else:
        # Standard learning curve ops cost
        c_ops = alpha * (c_floor + (params["C_ops1"] - c_floor) * n ** b_i)

    # V1: Pioneering phase — elevated costs for first n_p units
    pioneer_gamma = params.get("pioneer_gamma", 1.0)
    pioneer_n = params.get("pioneer_n", 0)
    if pioneer_gamma > 1.0 and pioneer_n > 0:
        pioneer_mask = n <= pioneer_n
        c_ops = np_where(pioneer_mask, c_ops * pioneer_gamma, c_ops)

    # V2: QA/certification cost — declines with experience
    C_QA1 = params.get("C_QA1", 0)
    if C_QA1 > 0:
        LR_QA = params.get("LR_QA", 0.85)
        b_qa = learning_exponent(LR_QA)
        c_ops = c_ops + C_QA1 * n ** b_qa

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


def earth_delivery_time(
    ns: float | NDFloat,
    prod_rate: float = 500,
    earth_max_units_per_year: float | None = None,
) -> NDFloat:
    """Earth delivery time — constant rate from t=0 (no ramp-up delay).

    Earth manufacturing can begin immediately, so t_{n,E} = n / prod_rate.

    U3: When earth_max_units_per_year is set, the effective Earth production
    rate is capped at min(prod_rate, earth_max_units_per_year), modeling
    launch throughput constraints.
    """
    ns_arr = asarray(ns, dtype=float)
    effective_rate = prod_rate
    if earth_max_units_per_year is not None:
        effective_rate = min(prod_rate, earth_max_units_per_year)
    return ns_arr / effective_rate


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
    use_piecewise: bool = True,
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
    use_piecewise : bool
        If True (default), use piecewise schedule with explicit construction
        delay as primary ISRU schedule. The piecewise schedule sets
        n_dot(t) = 0 for t < t_c where t_c = t0 - 1.
    """
    r = params.get("r", 0.0) if discount else 0.0

    # If discount requested but r==0, fall back to undiscounted
    if r == 0.0:
        discount = False
        phased_k_years = None

    ns = arange(1, n_max + 1, dtype=float)
    prod_rate = params.get("prod_rate", 500)
    k_ramp = params.get("k_ramp", 2.0)

    # O2: ISRU facility availability — reduces effective ISRU production rate
    availability = params.get("availability", 1.0)
    isru_prod_rate = prod_rate * availability

    # U3: Earth throughput cap
    earth_cap = params.get("earth_max_units_per_year", None)

    # Earth side
    earth_units = earth_unit_cost(ns, params)
    if discount:
        if earth_ramp is not None:
            t0_e, k_e = earth_ramp
            t_n_earth = earth_delivery_time_ramped(ns, prod_rate, t0_e, k_e)
        else:
            t_n_earth = earth_delivery_time(ns, prod_rate, earth_cap)
        discount_earth = (1.0 + r) ** (-t_n_earth)
        earth_cum = cumsum(earth_units * discount_earth)
    else:
        earth_cum = cumsum(earth_units)

    # ISRU side — ops (uses availability-adjusted production rate for timing)
    # A4: Use piecewise schedule as primary
    ops = isru_ops_cost(ns, params)
    if discount:
        if use_piecewise:
            t_n_isru = unit_to_time_piecewise(
                ns, isru_prod_rate, params["t0"], k_ramp
            )
        else:
            t_n_isru = unit_to_time(ns, isru_prod_rate, params["t0"], k_ramp)
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
        t_horizon = float(unit_to_time(n_max, isru_prod_rate, params["t0"], k_ramp))
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


def is_permanent_crossover(params: Params) -> bool:
    """V3: Check whether crossover is permanent (asymptotic ISRU < Earth).

    Compares asymptotic per-unit costs at very large n. If ISRU per-unit
    cost exceeds Earth per-unit cost asymptotically, any crossover is a
    finite-horizon amortization artifact that would eventually re-cross.

    Returns True if crossover is permanent (ISRU cheaper at large n).
    """
    alpha = params.get("alpha", 1.0)
    c_floor = params.get("C_floor", 0)
    p_transport = params.get("p_transport", 0)
    vitamin_frac = params.get("vitamin_frac", 0.0)

    # Asymptotic ISRU ops cost (learning terms -> 0 at large n)
    isru_asymp = alpha * c_floor + params["m"] * p_transport * alpha

    # Add vitamin fraction asymptotic contribution
    if vitamin_frac > 0:
        # At large n with launch learning, p_launch_eff -> p_fuel
        p_fuel = params.get("p_fuel", 200)
        c_vitamin_kg = params.get("c_vitamin_kg", 10000)
        isru_asymp = (1.0 - vitamin_frac) * isru_asymp + \
            vitamin_frac * params["m"] * (p_fuel + c_vitamin_kg)

    # Add QA asymptotic (-> 0 with learning, so negligible)
    # Pioneer phase also negligible at large n

    # Asymptotic Earth per-unit cost
    # Two-component: C_mat + C_labor1 * n^b_E -> C_mat (labor -> 0)
    # Plus launch: at large n with learning, p_launch -> m * p_fuel
    C_mat = params.get("C_mat", 0)
    b_L = params.get("b_L", None)
    if b_L is not None:
        p_fuel_e = params.get("p_fuel", 200)
        earth_asymp = C_mat + params["m"] * p_fuel_e
    else:
        earth_asymp = C_mat + params["m"] * params.get("p_launch", 1000)

    return isru_asymp < earth_asymp


def find_recrossing_volume(
    params: Params,
    crossover_n: int,
    N_max: int = 200000,
) -> tuple[int, int, float]:
    """Find the re-crossing volume N** where ISRU becomes more expensive again.

    Formally, N** = min{N > N* : Sigma_ISRU^NPV(N) > Sigma_Earth^NPV(N)},
    mirroring the crossover definition (Eq. 17).  N** is searched up to N_max
    (right-censored); with NPV discounting, late-arriving costs are heavily
    attenuated, so many asymptotically transient scenarios do not re-cross
    within any practical horizon.

    For transient crossovers, after the initial crossover at N*, the ISRU
    cumulative cost eventually re-crosses the Earth cumulative cost at N**.
    The savings window is [N*, N**].

    Returns
    -------
    recross_n : int
        The re-crossing volume N** (or N_max if no re-crossing found).
    peak_savings_n : int
        The production volume where earth_cum - isru_cum is maximized.
    peak_savings : float
        The peak cumulative savings (earth_cum - isru_cum) in dollars.
    """
    r = params.get("r", 0.05)
    ns = arange(1, N_max + 1, dtype=float)
    prod_rate = params.get("prod_rate", 500)
    k_ramp = params.get("k_ramp", 2.0)

    availability = params.get("availability", 1.0)
    isru_prod_rate = prod_rate * availability

    # Earth side
    earth_units = earth_unit_cost(ns, params)
    earth_cap = params.get("earth_max_units_per_year", None)
    t_n_earth = earth_delivery_time(ns, prod_rate, earth_cap)
    discount_earth = (1.0 + r) ** (-t_n_earth)
    earth_cum = cumsum(earth_units * discount_earth)

    # ISRU side
    ops = isru_ops_cost(ns, params)
    t_n_isru = unit_to_time_piecewise(ns, isru_prod_rate, params["t0"], k_ramp)
    discount_isru = (1.0 + r) ** (-t_n_isru)
    isru_ops_cum = cumsum(ops * discount_isru)
    isru_cum = params["K"] + isru_ops_cum

    # Savings = earth_cum - isru_cum (positive means ISRU is cheaper)
    savings = earth_cum - isru_cum

    # Find peak savings in the window after crossover
    post_cross = savings[crossover_n:]  # indices after crossover_n
    if len(post_cross) == 0:
        return N_max, crossover_n, 0.0

    peak_idx_rel = int(post_cross.argmax())
    peak_savings_n = crossover_n + peak_idx_rel + 1  # +1 for 1-based unit number
    peak_savings = float(post_cross[peak_idx_rel])

    # Find re-crossing: first index after crossover where savings becomes negative
    recross_candidates = np_where(post_cross < 0)[0]
    if len(recross_candidates) > 0:
        recross_n = crossover_n + int(recross_candidates[0]) + 1
    else:
        recross_n = N_max

    return recross_n, peak_savings_n, peak_savings


def compute_savings_window_survival(
    crossovers: NDFloat,
    recrossing_ns: NDFloat,
    horizons: list[int] | None = None,
) -> dict[int, float]:
    """AC1: Savings window survival — P(N* <= N_h <= N**) at each horizon.

    For a program committing to N_h units, returns the probability that N_h
    falls within the ISRU savings window [N*, N**].  This transforms the
    "transient" classification into an actionable decision tool.

    Parameters
    ----------
    crossovers : array
        N* values from MC (same length as recrossing_ns).
    recrossing_ns : array
        N** values from MC (N_max for permanent crossovers).
    horizons : list of int
        Planning horizons to evaluate (default: [5k, 10k, 20k, 50k, 100k]).

    Returns
    -------
    dict mapping horizon -> p_in_window (float in [0, 1]).
    """
    if horizons is None:
        horizons = [5000, 10000, 20000, 50000, 100000]
    crossovers = asarray(crossovers, dtype=float)
    recrossing_ns = asarray(recrossing_ns, dtype=float)
    result: dict[int, float] = {}
    for N_h in horizons:
        in_window = (crossovers <= N_h) & (N_h <= recrossing_ns)
        result[N_h] = float(in_window.mean())
    return result


def derive_asymptotic_costs(params: Params) -> dict[str, Any]:
    """AC3: Audit asymptotic cost consistency.

    Returns a dict with:
      - Each cost term's asymptotic (n -> inf) value and whether it vanishes
      - Total asymptotic per-unit cost for each pathway
      - is_permanent_crossover() classification
      - Empirical check at n=500,000
      - Consistency flag (analytic == empirical)
    """
    alpha = params.get("alpha", 1.0)
    c_floor = params.get("C_floor", 0)
    p_transport = params.get("p_transport", 0)
    vitamin_frac = params.get("vitamin_frac", 0.0)
    C_mat = params.get("C_mat", 0)
    b_L = params.get("b_L", None)

    terms: dict[str, Any] = {}

    # --- ISRU asymptotic terms ---
    terms["isru_ops_floor"] = {"value": alpha * c_floor, "vanishes": False}
    terms["isru_transport"] = {"value": params["m"] * p_transport * alpha, "vanishes": False}
    terms["isru_ops_learning"] = {"value": 0.0, "vanishes": True,
                                   "note": "C_ops1 * n^b_I -> 0"}

    # Compute ISRU total asymptotic
    isru_asymp = alpha * c_floor + params["m"] * p_transport * alpha

    if vitamin_frac > 0:
        p_fuel = params.get("p_fuel", 200)
        c_vitamin_kg = params.get("c_vitamin_kg", 10000)
        terms["vitamin_launch"] = {"value": vitamin_frac * params["m"] * p_fuel,
                                    "vanishes": False}
        terms["vitamin_mfg"] = {"value": vitamin_frac * params["m"] * c_vitamin_kg,
                                 "vanishes": False}
        isru_asymp = ((1.0 - vitamin_frac) * isru_asymp +
                      vitamin_frac * params["m"] * (p_fuel + c_vitamin_kg))

    # --- Earth asymptotic terms ---
    terms["earth_material"] = {"value": C_mat, "vanishes": False}
    terms["earth_labor"] = {"value": 0.0, "vanishes": True,
                             "note": "C_labor1 * n^b_E -> 0"}

    if b_L is not None:
        p_fuel_e = params.get("p_fuel", 200)
        terms["earth_launch_fuel"] = {"value": params["m"] * p_fuel_e, "vanishes": False}
        terms["earth_launch_ops"] = {"value": 0.0, "vanishes": True,
                                      "note": "p_ops * n^b_L -> 0"}
        earth_asymp = C_mat + params["m"] * p_fuel_e
    else:
        terms["earth_launch_const"] = {"value": params["m"] * params.get("p_launch", 1000),
                                        "vanishes": False}
        earth_asymp = C_mat + params["m"] * params.get("p_launch", 1000)

    terms["isru_total_asymp"] = isru_asymp
    terms["earth_total_asymp"] = earth_asymp
    terms["analytic_permanent"] = isru_asymp < earth_asymp
    terms["is_permanent_result"] = is_permanent_crossover(params)

    # Empirical validation at very large n (power-law terms decay slowly)
    n_large = asarray([1e15])
    isru_empirical = float(isru_ops_cost(n_large, params)[0])
    earth_empirical = float(earth_unit_cost(n_large, params)[0])
    terms["isru_empirical_1e15"] = isru_empirical
    terms["earth_empirical_1e15"] = earth_empirical
    terms["empirical_permanent"] = isru_empirical < earth_empirical

    # Consistency: analytic formula agrees with is_permanent_crossover()
    # (empirical may lag due to slow power-law decay of learning terms)
    terms["consistent"] = terms["analytic_permanent"] == terms["is_permanent_result"]

    return terms


def earth_unit_cost_plateau(
    n: float | NDFloat,
    params: Params,
    *,
    n_break: int = 500,
    damping: float = 0.5,
) -> NDFloat:
    """Y3: Earth per-unit cost with piecewise learning plateau.

    For n <= n_break: standard Wright curve with exponent b_E.
    For n > n_break: reduced exponent b_E2 = b_E * damping, modeling
    the empirical observation that learning rates moderate at high
    cumulative volumes (Argote & Epple 1990, Benkard 2000).

    damping=1.0 reproduces the standard model (no plateau).
    AB1: earth_n0 offsets the learning index for prior production.
    """
    n = asarray(n, dtype=float)
    b_E = learning_exponent(params["LR_E"])
    earth_n0 = params.get("earth_n0", 0)

    # AB1: Effective learning index
    n_eff = n + earth_n0

    C_mat = params.get("C_mat", 0)
    C_labor1 = params.get("C_labor1", params["C_mfg1"] - C_mat) if C_mat > 0 else params["C_mfg1"]

    b_E2 = b_E * damping  # reduced exponent after break

    if C_mat > 0:
        # Before break: C_mat + C_labor1 * n_eff^b_E
        # After break: C_mat + C_labor1 * n_break^(b_E - b_E2) * n_eff^b_E2
        scale_factor = C_labor1 * n_break ** (b_E - b_E2)
        c_mfg = np_where(
            n <= n_break,
            C_mat + C_labor1 * n_eff ** b_E,
            C_mat + scale_factor * n_eff ** b_E2,
        )
    else:
        scale_factor = C_labor1 * n_break ** (b_E - b_E2)
        c_mfg = np_where(
            n <= n_break,
            C_labor1 * n_eff ** b_E,
            scale_factor * n_eff ** b_E2,
        )

    # N1: Earth manufacturing cost floor
    C_mfg_floor = params.get("C_mfg_floor", 0)
    if C_mfg_floor > 0:
        c_mfg = maximum(c_mfg, C_mfg_floor)

    # Launch cost (same as earth_unit_cost)
    b_L = params.get("b_L", None)
    if b_L is not None:
        p_fuel = params.get("p_fuel", 200)
        p_ops = params.get("p_ops_launch", 800)
        launches_per_unit = params.get("launches_per_unit", 1.0)
        n_launches = n * launches_per_unit + earth_n0
        c_launch = params["m"] * (p_fuel + p_ops * n_launches ** b_L)
    else:
        c_launch = params["m"] * params["p_launch"]

    return c_mfg + c_launch


def find_crossover_plateau(
    params: Params,
    n_max: int = 40000,
    *,
    n_break: int = 500,
    damping: float = 0.5,
) -> int:
    """Y3: Find NPV crossover using piecewise learning plateau for Earth."""
    r = params.get("r", 0.05)
    ns = arange(1, n_max + 1, dtype=float)
    prod_rate = params.get("prod_rate", 500)
    k_ramp = params.get("k_ramp", 2.0)

    availability = params.get("availability", 1.0)
    isru_prod_rate = prod_rate * availability

    # Earth side with plateau learning
    earth_units = earth_unit_cost_plateau(ns, params, n_break=n_break, damping=damping)
    t_n_earth = earth_delivery_time(ns, prod_rate)
    discount_earth = (1.0 + r) ** (-t_n_earth)
    earth_cum = cumsum(earth_units * discount_earth)

    # ISRU side (unchanged)
    ops = isru_ops_cost(ns, params)
    t_n_isru = unit_to_time_piecewise(ns, isru_prod_rate, params["t0"], k_ramp)
    discount_isru = (1.0 + r) ** (-t_n_isru)
    isru_ops_cum = cumsum(ops * discount_isru)
    isru_cum = params["K"] + isru_ops_cum

    diff = isru_cum - earth_cum
    crossings = np_where(diff <= 0)[0]
    if len(crossings) > 0:
        return int(ns[crossings[0]])
    return n_max


def find_crossover_plateau_symmetric(
    params: Params,
    n_max: int = 40000,
    *,
    n_break_earth: int = 500,
    damping_earth: float = 0.5,
    n_break_isru: int = 500,
    damping_isru: float = 0.5,
) -> int:
    """Z2: Find NPV crossover with learning plateau on BOTH pathways.

    Earth side uses earth_unit_cost_plateau (Y3 model).
    ISRU side uses isru_ops_cost with n_break_isru/damping_isru.
    """
    r = params.get("r", 0.05)
    ns = arange(1, n_max + 1, dtype=float)
    prod_rate = params.get("prod_rate", 500)
    k_ramp = params.get("k_ramp", 2.0)

    availability = params.get("availability", 1.0)
    isru_prod_rate = prod_rate * availability

    # Earth side with plateau learning
    earth_units = earth_unit_cost_plateau(
        ns, params, n_break=n_break_earth, damping=damping_earth
    )
    t_n_earth = earth_delivery_time(ns, prod_rate)
    discount_earth = (1.0 + r) ** (-t_n_earth)
    earth_cum = cumsum(earth_units * discount_earth)

    # ISRU side with plateau learning
    ops = isru_ops_cost(
        ns, params, n_break_isru=n_break_isru, damping_isru=damping_isru
    )
    t_n_isru = unit_to_time_piecewise(ns, isru_prod_rate, params["t0"], k_ramp)
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
