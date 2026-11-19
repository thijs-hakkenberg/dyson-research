# Lunar flyby from a Sun–Earth L1 node: three-body study (rq-0-52)

Produced by `publications/scripts/run_cislunar_flyby.py` (model in `cislunar_flyby.py`) and
`run_cislunar_validation.py`.

- `reach.json` — excess speed (km/s) a tug reaches after leaving the node by way of the Moon,
  by node burn (50, 150, 300 m/s), time from the burn (45–200 days), longitude of the
  velocity from the Sun→Earth line (30° bins from −180°) and latitude from the ecliptic
  (0–15, 15–30, 30–45, 45–60, 60–90°). Read by `trajectory_opt.FlybyReach`. An arrival uses
  the mirror image.
- `summary.json` — counts, time to the first lunar encounter, fastest escapes.
- `validation.json` — the patched swingby against an integration with the Moon's gravity.
- `escapes.npz` (every escape found, 14 MB) is not stored; the run regenerates it in about
  ten minutes.
- `reach-launch.json` — the same table for a scout: launch that just reaches the Moon
  (C3 −1.8 to −0.2 km²/s²), one swingby, escape (`run_scout_flyby_model.py`).

## Halo node orbits and the inclined Moon (2026-11-15)

Produced by `run_cislunar_flyby_3d.py`.

- `reach-3d-planar-orbits.json`, `reach-3d-halo.json` — as `reach.json`, with two more
  dimensions: the angle of the Moon's ascending node from the Sun→Earth line at escape
  (60° bins) and signed latitude (−90 to 90°). One swingby. An arrival reads node angle
  180° − node with the velocity's out-of-ecliptic part reversed.
- `summary-3d.json` — orbits, encounters, reach by latitude and by node angle.
- `summary-3d-inc0.json` — the check run with no inclination, which reproduces the planar
  model's single-swingby tables exactly.
- `reach-launch-low.json` — the scout launch table for C3 ≤ −1.0 km²/s².
- `reach-3d-station-{halo-120,halo-300,planar-100}.json` — reach for one node orbit each, with
  one more dimension in front: where the station is on that orbit at the moment of escape
  (eighths of the period from the Sun-side crossing of the Sun–Earth line). From
  `run_cislunar_flyby_3d.py --station` (32 places × 48 burn directions). An arrival reads
  the place counted backwards. `summary-3d-station.json` is that run's summary.
- `station-reach-convergence.json` — mean in-plane reach of those tables with all, half, a
  quarter and an eighth of the escapes: they are not converged (3–4% per halving).
- `arrival-check.json` — arrivals flown forwards from the mirror image of departures
  (`run_flyby_arrival_check.py`): errors at the Moon and at the node orbit.
- `escapes-3d*.npz` are not stored (88 MB and more); the runs take 20 to 30 minutes.
