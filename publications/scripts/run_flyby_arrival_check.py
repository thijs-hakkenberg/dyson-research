"""
rq-0-52: the return to a halo node by way of the Moon, flown forwards.

    python run_flyby_arrival_check.py

The tug legs take the reach of an arrival as the mirror image of the reach of a departure
(cislunar_flyby.mirror). This flies a sample of arrivals forwards in time and checks each
step against the unmirrored model:

  1. from the edge of the Earth's sphere of influence to the Moon's orbital distance, where
     the path must lie in the Moon's orbit plane, with the node line at 180° − node;
  2. a swingby of the prograde Moon there, within the turn the lowest pass allows;
  3. from the Moon to the node orbit, where the place must be on the same northern halo
     orbit and the insertion burn must be within the budget;
  4. the direction, node angle and station place under which trajectory_opt.FlybyReach looks
     the arrival up must be those of the departure it is the image of.

Writes publications/data/cislunar-flyby/arrival-check.json.
"""

from __future__ import annotations

import json
import os

import numpy as np

import cislunar_flyby as c
from run_cislunar_flyby import OUT, T_ENCOUNTER, T_TOTAL
from trajectory_opt import FlybyReach

KM = c.AU_KM


def check(az_km=300e3, dv_ms=300.0, share=0.8, node0=np.radians(60.0), n_phase=8, n_az=12, n_up=9, fan=(4, 8), kind='halo'):
    state, period = c.halo_orbit(az_km) if kind == 'halo' else c.lyapunov_orbit(az_km)
    pts = c.orbit_points(state, period, n_phase)
    base = np.repeat(pts, n_az, axis=0)
    phase = np.repeat(np.arange(n_phase) / n_phase, n_az)
    az = np.tile(np.arange(n_az) * 2 * np.pi / n_az, n_phase)
    ups = np.linspace(-1.0, 1.0, n_up) * np.sqrt(1 - share**2)
    ce, el, yc, tc = c.encounters_inclined(base, az, ups, dv_ms, node0, T_ENCOUNTER * c.DAY, inplane=share)
    states, src = c.swingby_fan_inclined(yc, tc, node0, *fan)
    f = c.integrate(states, tc[src], T_TOTAL * c.DAY)
    ok = f.status == 1
    v, lon, lat, c3 = c.escape_state(f.y[ok])
    keep = c3 > 0
    src, te, y_esc, post = src[ok][keep], f.t[ok][keep], f.y[ok][keep], states[ok][keep]
    v, lon, lat = v[keep], lon[keep], lat[keep]
    n = len(src)

    # ---- the arrival, forwards in time: starts at −te, node line at π − node0
    node_arr = np.pi - node0
    a1 = c.integrate(c.mirror(y_esc), -te, -tc[src], stop_at_escape=False)
    want = c.mirror(post)
    pos1 = np.linalg.norm(a1.y[:, :3] - want[:, :3], axis=1) * KM
    vel1 = np.linalg.norm(a1.y[:, 3:] - want[:, 3:], axis=1) * c.VU_KMS * 1e3
    good = (a1.status == 0) & (pos1 < 500.0)
    miss = np.abs(c.plane_miss(a1.y, a1.t, node_arr)) * KM
    radius = np.abs(c._radius(a1.y) - c.A_MOON) * KM
    w_in, _, _ = c.encounter_vinf_inclined(a1.y, a1.t, node_arr)
    after = c.mirror(yc[src])  # the departure's approach to the Moon is the arrival's path away from it
    w_out, _, _ = c.encounter_vinf_inclined(after, -tc[src], node_arr)
    s_in, s_out = np.linalg.norm(w_in, axis=1), np.linalg.norm(w_out, axis=1)
    turn = np.arccos(np.clip(np.sum(w_in * w_out, axis=1) / (s_in * s_out), -1, 1))
    a2 = c.integrate(after, -tc[src], 0.0, stop_at_escape=False)
    home = c.mirror(base[ce[src]])
    pos2 = np.linalg.norm(a2.y[:, :3] - home[:, :3], axis=1) * KM
    burn = np.linalg.norm(a2.y[:, 3:] - home[:, 3:], axis=1) * c.VU_KMS * 1e3
    # the mirrored place is on the same orbit, at minus the phase
    k = np.round(phase[ce[src]] * n_phase).astype(int)
    orbit_pos = np.linalg.norm(home[:, :3] - pts[(-k) % n_phase][:, :3], axis=1) * KM
    orbit_vel = np.linalg.norm(home[:, 3:] - pts[(-k) % n_phase][:, 3:], axis=1) * c.VU_KMS * 1e3

    # ---- what the leg solver would look up for this arrival
    start = c.mirror(y_esc)
    va, lon_a, lat_a, _ = c.escape_state(start)  # the incoming velocity, non-rotating axes
    rc = FlybyReach.__new__(FlybyReach)
    rc.signed = True
    look = np.array([rc.angles(np.array([np.cos(np.radians(b)) * np.cos(np.radians(l)), np.cos(np.radians(b)) * np.sin(np.radians(l)), np.sin(np.radians(b))]),
                               np.array([1.0, 0.0, 0.0]), True) for l, b in zip(lon_a, lat_a)])
    dlon = np.abs((look[:, 0] - lon + 180.0) % 360.0 - 180.0)
    dlat = np.abs(look[:, 1] - lat)
    node_dep = np.degrees(node0 - te) % 360.0  # as tabulated
    node_seen = np.degrees(node_arr + te) % 360.0  # node angle on the day the arrival enters
    dnode = np.abs((180.0 - node_seen - node_dep + 180.0) % 360.0 - 180.0)
    station_dep = (phase[ce[src]] + te / period) % 1.0
    station_seen = (-phase[ce[src]] - te / period) % 1.0  # where the station is on that day
    dstation = np.abs(((-station_seen) % 1.0 - station_dep + 0.5) % 1.0 - 0.5)

    g = good
    mx = lambda a: float(np.max(a[g])) if g.any() else None
    return {
        'orbit': {'kind': kind, 'size_km': az_km, 'period_days': round(period * c.TU_DAYS, 2)}, 'burn_ms': dv_ms, 'node_deg_at_burn': float(np.degrees(node0)),
        'departures_with_escape': int(n), 'arrivals_reaching_the_moon_as_mirrored': int(g.sum()),
        'arrivals_lost_to_integration_error': int(n - g.sum()),
        'at_the_moon': {'max_position_error_km': mx(pos1), 'max_velocity_error_ms': mx(vel1), 'max_distance_from_moon_plane_km': mx(miss),
                        'max_distance_from_moon_orbit_radius_km': mx(radius),
                        'max_excess_speed_change_ms': mx(np.abs(s_in - s_out) * c.VU_KMS * 1e3),
                        'max_turn_over_allowed': mx(turn / c.max_turn(s_in))},
        'at_the_node': {'max_position_error_km': mx(pos2), 'max_insertion_burn_ms': mx(burn), 'budget_ms': dv_ms,
                        'max_distance_of_image_from_orbit_km': mx(orbit_pos), 'max_velocity_difference_from_orbit_ms': mx(orbit_vel)},
        'lookup': {'max_longitude_error_deg': mx(dlon), 'max_latitude_error_deg': mx(dlat), 'max_node_angle_error_deg': mx(dnode),
                   'max_station_place_error': mx(dstation)},
        'excess_speed_kms': {'min': mx(-v) and -mx(-v), 'max': mx(v)},
    }


def main():
    out = {'model': 'arrivals flown forwards from the mirror image of departures; see run_flyby_arrival_check.py',
           'cases': [check(300e3, 300.0), check(120e3, 150.0, node0=np.radians(200.0)), check(100e3, 150.0, node0=np.radians(310.0), kind='planar')]}
    json.dump(out, open(os.path.join(OUT, 'arrival-check.json'), 'w'), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == '__main__':
    main()
