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
