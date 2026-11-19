"""Directly solved legs written for the chain model (run_phase0_chain_direct.py)."""

import csv
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import run_phase0_chain_direct as m  # noqa: E402

COLS = ('target', 'leg', 'burn_ms', 'budget', 'depart', 'tof', 'dv', 'vinf', 'lon', 'lat', 'allowance', 'delivered', 'dv_eff', 'node_T',
        'flight_days', 'burn_frac', 'escape_shift_days', 'runs', 'timed_out', 'seconds')


def test_legs_carry_the_direct_node_dates_and_charged_dv(tmp_path, monkeypatch):
    jd = m.J2000 + 10000.0
    table = tmp_path / 'table.csv'
    with open(table, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(m.COLUMNS)
        for leg in ('out', 'in'):
            w.writerow(['X', 300, 105, leg, 2000.0 + 10000.0 / 365.25, 200.0, 0, 4.0, 4.5, 0.5, 1.2, 10.0, 5.0, 119.8])
    direct = tmp_path / f'node-legs-direct-{m.ORBIT}-p0{m.TAG}-legs.csv'
    with open(direct, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(COLS)
        base = dict(target='X', burn_ms=300, budget=105.0, depart=jd, tof=200.0, dv=4.0, vinf=1.2, lon=10.0, lat=5.0, allowance=119.8,
                    flight_days=90.0, burn_frac=1.0, escape_shift_days=0.0, runs=1, timed_out=False, seconds=1.0)
        w.writerow([dict(base, leg='out', delivered=1.0, dv_eff=4.2, node_T=10000.0 - 95.0).get(k) for k in COLS])
        w.writerow([dict(base, leg='in', delivered=1.2, dv_eff=4.0, node_T=10000.0 + 200.0 + 80.0).get(k) for k in COLS])
        w.writerow([dict(base, leg='in', tof=300.0, delivered=0.0, dv_eff=float('inf'), node_T=float('nan')).get(k) for k in COLS])
    monkeypatch.setattr(m, 'TRAJ', str(tmp_path))
    monkeypatch.setattr(m, 'TABLE_LEGS', str(table))
    path, counts = m.write_legs(0, m.table_rows())
    assert counts == {'legs': 3, 'flown': 2, 'unmatched': 0}
    rows = {r['leg']: r for r in csv.DictReader(open(path))}
    assert float(rows['out']['allowance_days']) == 95.0 and float(rows['in']['allowance_days']) == 80.0
    assert float(rows['out']['low_thrust_kms']) == 4.2 and abs(float(rows['out']['thrust_fraction']) - 0.525) < 1e-9
