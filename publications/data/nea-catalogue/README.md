# NEA catalogue (rq-0-52)

- `sbdb_neo_raw.json.gz` — all near-Earth asteroids from the JPL Small-Body Database Query API
  (`sb-group=neo`, `sb-kind=a`), retrieved 2026-10-25: orbital elements, H, diameter, albedo,
  rotation period and SMASS/Tholen taxonomy where known. 42,806 objects. Re-fetch with:

  ```bash
  curl -G https://ssd-api.jpl.nasa.gov/sbdb_query.api \
    --data-urlencode "fields=spkid,full_name,pdes,epoch,e,a,q,i,om,w,ma,H,diameter,albedo,rot_per,spec_B,spec_T,class,condition_code" \
    --data-urlencode "sb-group=neo" --data-urlencode "sb-kind=a" -o sbdb_neo_raw.json
  ```

- `candidates.csv`, `summary.json` — output of `publications/scripts/run_nea_accessibility.py`.

Data: NASA/JPL Solar System Dynamics (public domain).
