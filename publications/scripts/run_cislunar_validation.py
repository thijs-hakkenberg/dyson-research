"""
rq-0-52: check the patched lunar swingby of cislunar_flyby.py against an integration with
the Moon's gravity acting throughout.

    python run_cislunar_validation.py

For a sample of first encounters it takes the same approach trajectory four days before
the encounter, spreads small aim corrections over the Moon's B-plane, and flies every one
of them past a gravitating Moon to escape. The envelope of excess speed against direction
is then compared with the one the patched model gives for that encounter.

Writes publications/data/cislunar-flyby/validation.json.
"""

from __future__ import annotations

import json
import os

import numpy as np

import cislunar_flyby as c
from run_cislunar_flyby import OUT, T_TOTAL

LEAD_DAYS = 4.0
LON = np.arange(-180.0, 181.0, 30.0)


def envelope(v, lon, lat):
    """Largest excess speed per 30° of longitude, for escapes within 15° of the ecliptic."""
    out = np.zeros(len(LON) - 1)
    k = np.clip(np.digitize(lon, LON) - 1, 0, len(out) - 1)
    sel = np.abs(lat) <= 15
    np.maximum.at(out, k[sel], v[sel])
    return out


def one(y_dep, t_enc, yc):
    vinf, vm, th = c.encounter_vinf(yc[None])
    # patched model
    fan, idx = c.swingby_fan(yc[None], 24, 25)
    f = c.integrate(fan, t_enc, t_enc + 60 * c.DAY)
    ok = f.status == 1
    vp, lp, bp, c3 = c.escape_state(f.y[ok])
    # with the Moon: back up along the approach, then spread aim points over the B-plane
    t0 = t_enc - LEAD_DAYS * c.DAY
    y0 = c.integrate(y_dep[None], 0.0, t0, stop_at_escape=False).y[0]
    u = vinf[0] / np.linalg.norm(vinf[0])
    p = np.cross([0, 0, 1.0], u)
    p /= np.linalg.norm(p)
    q = np.cross(u, p)
    b = np.geomspace(3000.0, 80000.0, 90) / c.AU_KM
    ang = np.arange(0, 360, 5) * np.pi / 180
    B, A = np.meshgrid(b, ang, indexing='ij')
    dv = (B.ravel()[:, None] * (np.cos(A.ravel())[:, None] * p + np.sin(A.ravel())[:, None] * q)) / (LEAD_DAYS * c.DAY)
    y = np.repeat(y0[None], len(dv), axis=0)
    y[:, 3:] += dv
    moon0 = th[0] - (c.N_MOON - 1.0) * t_enc
    g = c.integrate(y, t0, t_enc + 60 * c.DAY, moon=np.full(len(y), moon0))
    okm = (g.status == 1) & (g.moon_min >= c.R_PERILUNE) & (g.moon_min < 60000 / c.AU_KM)
    vmn, lm, bm, c3m = c.escape_state(g.y[okm])
    ep, em = envelope(vp[c3 > 0], lp[c3 > 0], bp[c3 > 0]), envelope(vmn[c3m > 0], lm[c3m > 0], bm[c3m > 0])
    both = (ep > 0) & (em > 0)
    return {
        'moon_relative_speed_kms': round(float(np.linalg.norm(vinf[0]) * c.VU_KMS), 3),
        'max_vinf_patched': round(float(vp.max()) if len(vp) else 0.0, 3),
        'max_vinf_with_moon': round(float(vmn.max()) if len(vmn) else 0.0, 3),
        'max_latitude_patched_deg': round(float(np.abs(bp[c3 > 0]).max()) if (c3 > 0).any() else 0.0, 1),
        'max_latitude_with_moon_deg': round(float(np.abs(bm[c3m > 0]).max()) if (c3m > 0).any() else 0.0, 1),
        'direction_bins_compared': int(both.sum()),
        'mean_abs_envelope_difference_kms': round(float(np.abs(ep - em)[both].mean()), 3) if both.any() else None,
        'bins_only_patched': int(((ep > 0) & (em == 0)).sum()), 'bins_only_with_moon': int(((em > 0) & (ep == 0)).sum()),
    }


def main():
    rng = np.random.default_rng(3)
    cases = []
    for dv in (50.0, 150.0, 300.0):
        ys = np.concatenate([c.node_departures(ax, 8, 12, dv)[0] for ax in (20e3, 200e3)])
        f = c.integrate(ys, 0.0, T_TOTAL * c.DAY, crossings=2)
        rows = np.nonzero(np.isfinite(f.t_cross[:, 0]))[0]
        for r in rng.choice(rows, size=min(5, len(rows)), replace=False):
            k = int(rng.integers(0, 2)) if np.isfinite(f.t_cross[r, 1]) else 0
            res = one(ys[r], f.t_cross[r, k], f.y_cross[r, k])
            res['burn_ms'] = dv
            cases.append(res)
            print(res, flush=True)
    a = np.array([[x['max_vinf_patched'], x['max_vinf_with_moon']] for x in cases if x['max_vinf_patched'] > 0])
    d = [x['mean_abs_envelope_difference_kms'] for x in cases if x['mean_abs_envelope_difference_kms'] is not None]
    out = {'cases': cases, 'cases_where_patched_model_finds_no_escape': sum(1 for x in cases if x['max_vinf_patched'] == 0), 'max_vinf_ratio_with_moon_to_patched': {'min': round(float((a[:, 1] / a[:, 0]).min()), 3), 'median': round(float(np.median(a[:, 1] / a[:, 0])), 3),
                                                                    'max': round(float((a[:, 1] / a[:, 0]).max()), 3)},
           'mean_envelope_difference_kms': round(float(np.mean(d)), 3)}
    json.dump(out, open(os.path.join(OUT, 'validation.json'), 'w'), indent=1)
    print(json.dumps({k: v for k, v in out.items() if k != 'cases'}, indent=1))


if __name__ == '__main__':
    main()
