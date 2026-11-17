"""Target count with several stations on the node orbit (run_node_stations_direct.py)."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import run_node_stations_direct as s  # noqa: E402


def leg(kind, place, depart, node_T, dv=4.0, tof=100.0):
    return {'leg': kind, 'place': place, 'depart': depart, 'tof': tof, 'dv_eff': dv, 'node_T': node_T}


def test_station_sets_cover_every_rotation():
    assert s.station_sets(1) == [(k,) for k in range(8)]
    assert s.station_sets(2) == [(0, 4), (1, 5), (2, 6), (3, 7)]
    assert s.station_sets(8) == [tuple(range(8))]


def test_a_cycle_can_leave_from_one_station_and_return_to_another():
    rows = [leg('out', 0, 1000.0, 990.0), leg('in', 4, 1500.0, 1700.0), leg('in', 0, 1500.0, 1700.0, dv=6.0)]
    assert s.best_cycle(rows, (0,)) is None  # the return to station 0 is over the leg cap
    assert abs(s.best_cycle(rows, (0, 4)) - 710.0 / 365.25) < 1e-12
    assert s.best_cycle(rows, (0, 4), same_station=True) is None


def test_stay_and_cycle_caps_hold():
    short_stay = [leg('out', 0, 1000.0, 990.0), leg('in', 0, 1120.0, 1300.0)]  # back after 20 days at the target
    assert s.best_cycle(short_stay, (0,)) is None
    too_long = [leg('out', 0, 1000.0, 990.0), leg('in', 0, 2000.0, 990.0 + 4.1 * 365.25)]
    assert s.best_cycle(too_long, (0,)) is None
