"""Water extraction cost model for Paper 05: ISRU Water Extraction.

Version 2.0: Transport cost derived from physics (Tsiolkovsky equation + fleet
economics) rather than sampled independently. Adds trip time modeling and
working capital cost for water-in-transit.

Pure math module — no matplotlib, no prints.
"""

from __future__ import annotations

__version__ = "2.0.0"

from typing import Any
from numpy import (
    floating, log, maximum, asarray, arange, ones_like, zeros_like,
    exp as np_exp, where as np_where, cumsum, log1p, minimum, array,
    linspace, ndarray,
)
from numpy.typing import NDArray

NDFloat = NDArray[floating[Any]]
Params = dict[str, Any]

G0 = 9.80665  # standard gravity (m/s^2)

# ---------------------------------------------------------------------------
# Transport physics
# ---------------------------------------------------------------------------

def payload_fraction(delta_v_km_s: float, Isp_s: float) -> float:
    """Payload mass fraction from the Tsiolkovsky equation.

    f_payload = 1 / mass_ratio = exp(-delta_v / (Isp * g0))
    """
    v_e = Isp_s * G0  # exhaust velocity (m/s)
    delta_v = delta_v_km_s * 1000.0  # convert to m/s
    mass_ratio = np_exp(delta_v / v_e)
    return float(1.0 / mass_ratio)


def trip_time_years(delta_v_km_s: float, thrust_N: float, vehicle_mass_kg: float) -> float:
    """Approximate one-way trip time for low-thrust transfer.

    Uses constant-thrust approximation: t = m * delta_v / F
    Real trajectories are longer due to gravity losses; multiply by 1.5 factor.
    """
    delta_v = delta_v_km_s * 1000.0
    accel = thrust_N / vehicle_mass_kg
    t_seconds = delta_v / accel * 1.5  # 1.5x gravity loss factor
    return t_seconds / (365.25 * 86400)


def transport_cost_per_kg_derived(p: Params) -> float:
    """Derive transport cost from vehicle economics and physics.

    Cost per kg = (vehicle_amortized_cost_per_trip + propellant_cost) / payload_per_trip
    """
    f_pay = payload_fraction(p["delta_v_to_L4L5"], p["Isp"])
    payload_per_trip = p["vehicle_capacity_kg"] * f_pay

    # Vehicle amortized cost per trip
    vehicle_cost = p["vehicle_cost"]
    vehicle_trips = p["vehicle_lifetime_trips"]
    amortized = vehicle_cost / vehicle_trips

    # Propellant cost (propellant mass = payload * (1/f_pay - 1) * prop_fraction)
    prop_mass = payload_per_trip * (1.0 / f_pay - 1.0)
    prop_cost = prop_mass * p.get("propellant_cost_per_kg", 0)  # 0 for EP (xenon negligible)

    # Operations cost per trip
    ops_per_trip = p.get("ops_cost_per_trip", 0)

    if payload_per_trip <= 0:
        return float('inf')
    return (amortized + prop_cost + ops_per_trip) / payload_per_trip


# ---------------------------------------------------------------------------
# Baseline parameters for water extraction sources
# ---------------------------------------------------------------------------

ASTEROID_BASELINE: Params = {
    # Extraction parameters
    "water_fraction": 0.10,          # mass fraction of extractable water (CI chondrite ~10%)
    "extraction_yield": 0.70,        # fraction of water actually recovered
    "extraction_energy_kWh_per_kg": 2.5,  # thermal energy per kg water extracted
    "extraction_rate_kg_per_hr": 50, # kg water/hr at full operation
    "availability": 0.85,            # fraction of time the system operates

    # Capital costs
    "K_extraction": 5e9,             # extraction system capital ($)
    "K_transport": 10e9,             # transport vehicle fleet capital ($)
    "K_anchoring": 0.5e9,            # anchoring/excavation system capital ($)
    "K_processing": 2e9,             # water purification & electrolysis capital ($)

    # Operating costs
    "C_ops_per_kg": 200,             # operating cost per kg water ($/kg)
    "LR_ops": 0.90,                  # operations learning rate

    # Transport — now physics-derived
    "delta_v_to_L4L5": 4.5,          # km/s from NEA to L4/L5
    "Isp": 2500,                     # Hall thruster Isp (s)
    "vehicle_capacity_kg": 50_000,   # vehicle wet mass (kg)
    "vehicle_cost": 500e6,           # cost per transport vehicle ($)
    "vehicle_lifetime_trips": 20,    # trips before replacement
    "propellant_cost_per_kg": 0,     # EP propellant cost negligible
    "ops_cost_per_trip": 2e6,        # mission ops per trip ($)
    "thrust_N": 2.0,                 # total EP thrust (N)

    # Production targets
    "target_annual_kg": 500_000,     # 500 tonnes/year target
    "ramp_years": 5,                 # years to reach full production
    "program_years": 30,             # total program duration

    # Financial
    "r": 0.05,                       # discount rate
}

LUNAR_BASELINE: Params = {
    "water_fraction": 0.05,
    "extraction_yield": 0.60,
    "extraction_energy_kWh_per_kg": 4.0,
    "extraction_rate_kg_per_hr": 100,
    "availability": 0.80,

    "K_extraction": 8e9,
    "K_transport": 15e9,
    "K_anchoring": 0.2e9,
    "K_processing": 3e9,
    "K_surface_base": 5e9,

    "C_ops_per_kg": 350,
    "LR_ops": 0.88,

    # Transport — chemical from lunar surface
    "delta_v_to_L4L5": 2.5,
    "Isp": 450,                      # chemical
    "vehicle_capacity_kg": 30_000,
    "vehicle_cost": 300e6,
    "vehicle_lifetime_trips": 10,    # chemical vehicles wear faster
    "propellant_cost_per_kg": 5,     # LOX/LH2 from ISRU (cheap if available)
    "ops_cost_per_trip": 5e6,        # higher ops for crewed-proximate operations
    "thrust_N": 50_000,              # chemical thrust (high)

    "target_annual_kg": 500_000,
    "ramp_years": 5,
    "program_years": 30,
    "r": 0.05,
}

PHOBOS_BASELINE: Params = {
    "water_fraction": 0.03,
    "extraction_yield": 0.50,
    "extraction_energy_kWh_per_kg": 3.0,
    "extraction_rate_kg_per_hr": 30,
    "availability": 0.75,

    "K_extraction": 12e9,
    "K_transport": 25e9,
    "K_anchoring": 0.8e9,
    "K_processing": 3e9,

    "C_ops_per_kg": 500,
    "LR_ops": 0.92,

    "delta_v_to_L4L5": 6.0,
    "Isp": 2500,
    "vehicle_capacity_kg": 50_000,
    "vehicle_cost": 800e6,
    "vehicle_lifetime_trips": 10,
    "propellant_cost_per_kg": 0,
    "ops_cost_per_trip": 5e6,
    "thrust_N": 2.0,

    "target_annual_kg": 500_000,
    "ramp_years": 8,
    "program_years": 30,
    "r": 0.05,
}


# ---------------------------------------------------------------------------
# S-curve ramp-up
# ---------------------------------------------------------------------------

def ramp_fraction(t: NDFloat, t0: float, k: float = 2.0) -> NDFloat:
    """Logistic S-curve ramp from 0 to 1."""
    return 1.0 / (1.0 + np_exp(-k * (t - t0)))


# ---------------------------------------------------------------------------
# Annual production
# ---------------------------------------------------------------------------

def annual_production(p: Params) -> NDFloat:
    """Annual water production in kg, accounting for ramp-up."""
    years = arange(p["program_years"])
    frac = ramp_fraction(years, p["ramp_years"] / 2.0)
    max_annual = (
        p["extraction_rate_kg_per_hr"]
        * p["availability"]
        * 8760
        * p["extraction_yield"]
    )
    return minimum(frac * p["target_annual_kg"], max_annual * ones_like(years))


# ---------------------------------------------------------------------------
# Cost functions
# ---------------------------------------------------------------------------

def total_capital(p: Params) -> float:
    """Total upfront capital investment."""
    K = p["K_extraction"] + p["K_transport"] + p["K_anchoring"] + p["K_processing"]
    if "K_surface_base" in p:
        K += p["K_surface_base"]
    return K


def annual_ops_cost(p: Params, cumulative_kg: NDFloat) -> NDFloat:
    """Annual operating cost with learning curve."""
    b = log(p["LR_ops"]) / log(2)
    cost_per_kg = p["C_ops_per_kg"] * maximum(cumulative_kg / 1000.0, 1.0) ** b
    prod = annual_production(p)
    return cost_per_kg * prod


def get_trip_time(p: Params) -> float:
    """One-way trip time in years."""
    return trip_time_years(p["delta_v_to_L4L5"], p["thrust_N"], p["vehicle_capacity_kg"])


def annual_transport_cost(p: Params) -> NDFloat:
    """Annual transport cost derived from vehicle economics and physics."""
    prod = annual_production(p)
    cost_per_kg = transport_cost_per_kg_derived(p)
    return prod * cost_per_kg


def annual_transit_capital_cost(p: Params) -> NDFloat:
    """Working capital cost for water tied up in transit.

    Water in transit cannot be used — this is an opportunity cost
    modeled as interest on the value of water-in-transit.
    """
    prod = annual_production(p)
    tt = get_trip_time(p)
    # Average water in transit = annual_production * trip_time (one-way)
    # Round-trip means vehicle is unavailable for 2*trip_time
    # Value of water in transit ≈ production_cost * quantity_in_transit
    cpk = transport_cost_per_kg_derived(p)
    water_in_transit = prod * min(tt * 2, 1.0)  # cap at 1 year
    return water_in_transit * p["r"] * cpk  # opportunity cost


def total_cost_trajectory(p: Params) -> tuple[NDFloat, NDFloat, NDFloat]:
    """Compute annual and cumulative cost trajectory."""
    prod = annual_production(p)
    cum_prod = cumsum(prod)

    ops = annual_ops_cost(p, cum_prod)
    transport = annual_transport_cost(p)
    transit_cost = annual_transit_capital_cost(p)

    annual = ops + transport + transit_cost
    annual_with_capex = annual.copy()
    annual_with_capex[0] += total_capital(p)

    cumulative = cumsum(annual_with_capex)
    return annual_with_capex, cumulative, cum_prod


def cost_per_kg_trajectory(p: Params) -> NDFloat:
    """Cost per kg of water delivered over time, including amortized capital."""
    _, cum_cost, cum_prod = total_cost_trajectory(p)
    return np_where(cum_prod > 0, cum_cost / cum_prod, 0.0)


def npv_cost(p: Params) -> float:
    """Net present value of total program cost."""
    annual, _, _ = total_cost_trajectory(p)
    years = arange(p["program_years"])
    discount = (1 + p["r"]) ** (-years)
    return float((annual * discount).sum())


def npv_cost_per_kg(p: Params) -> float:
    """NPV cost per kg of water delivered."""
    annual, _, cum_prod = total_cost_trajectory(p)
    years = arange(p["program_years"])
    discount = (1 + p["r"]) ** (-years)
    total_npv = float((annual * discount).sum())
    total_prod = float(cum_prod[-1])
    if total_prod == 0:
        return float('inf')
    return total_npv / total_prod


# ---------------------------------------------------------------------------
# Source comparison
# ---------------------------------------------------------------------------

def compare_sources(sources: dict[str, Params] | None = None) -> dict[str, dict[str, float]]:
    """Compare multiple water sources on key metrics."""
    if sources is None:
        sources = {
            "C-type NEA": ASTEROID_BASELINE,
            "Lunar polar ice": LUNAR_BASELINE,
            "Phobos/Deimos": PHOBOS_BASELINE,
        }

    results = {}
    for name, params in sources.items():
        _, cum_cost, cum_prod = total_cost_trajectory(params)
        f_pay = payload_fraction(params["delta_v_to_L4L5"], params["Isp"])
        tt = get_trip_time(params)
        derived_cpk = transport_cost_per_kg_derived(params)
        results[name] = {
            "total_capital": total_capital(params),
            "npv_total": npv_cost(params),
            "npv_per_kg": npv_cost_per_kg(params),
            "total_production_kg": float(cum_prod[-1]),
            "year_10_cost_per_kg": float(
                cost_per_kg_trajectory(params)[min(9, params["program_years"] - 1)]
            ),
            "year_20_cost_per_kg": float(
                cost_per_kg_trajectory(params)[min(19, params["program_years"] - 1)]
            ),
            "delta_v": params["delta_v_to_L4L5"],
            "payload_fraction": f_pay,
            "derived_transport_cost_per_kg": derived_cpk,
            "trip_time_years": tt,
        }
    return results


def optimal_source_by_scale(scales: NDFloat | None = None) -> dict[str, list[float]]:
    """Find optimal source as function of annual production target."""
    if scales is None:
        scales = asarray([1e4, 5e4, 1e5, 2.5e5, 5e5, 1e6, 2e6])

    result: dict[str, list[float]] = {"scales": list(scales)}
    for name, baseline in [
        ("C-type NEA", ASTEROID_BASELINE),
        ("Lunar polar ice", LUNAR_BASELINE),
        ("Phobos/Deimos", PHOBOS_BASELINE),
    ]:
        costs = []
        for scale in scales:
            p = dict(baseline)
            p["target_annual_kg"] = float(scale)
            costs.append(npv_cost_per_kg(p))
        result[name] = costs

    return result
