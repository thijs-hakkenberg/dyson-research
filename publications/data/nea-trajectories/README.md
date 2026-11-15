# Asteroid trajectory study (rq-0-52, second pass)

Produced by `publications/scripts/run_trajectory_study.py` on 2026-11-12 from the JPL SBDB
catalogue in `../nea-catalogue/`.

| File | Contents |
|---|---|
| `summary.json` | Counts by tug Δv cap, cycle limit and lunar-flyby setting; scout counts; assumptions |
| `targets.csv` | One row per shortlisted asteroid (150, H ≤ 22): scout Δv by departure option, shortest tug cycle by flyby setting and leg cap, leg Δv, first departure and departure years with a cycle ≤ 4 yr |
| `legs.csv` | Every feasible optimised tug leg: departure, flight time, revolutions, impulsive and low-thrust Δv, thrust fraction |
| `stage1.npz` | Cached stage 1 (impulsive) results for all 1,263 prefiltered asteroids; delete or pass `--fresh` to recompute |

`lga` columns give the Earth-relative excess speed (km/s) a lunar flyby is assumed to provide.
That figure is an unsourced assumption; see the limits listed in rq-0-52.

## Scout launch trade (2026-11-15)

Produced by `run_scout_launch_sweep.py` then `run_scout_launch_trade.py`.

| File | Contents |
|---|---|
| `scout-launch-sweep.json` | Least-Δv scout transfer per target and launch option (C3 = 0, lunar swingby from two launch energies, C3 = 2 to 20); every solution for C3 = 10 |
| `scout-launch-sweep.csv` | The same as one row per target: scout Δv and flight time by launch option |
| `scout-launch-trade.json` | Counts by launch option and scout Δv budget, alone and with the tug sets; shared-launch pairs; Earth-loop option; scout mass and thruster hours; perigee kick; launcher payload estimate |

The launcher payloads are an estimate from published figures, not a provider's curve.
