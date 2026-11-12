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
