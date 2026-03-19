# Revision Plan: Paper 05 Version B

## Review Summary (Version A)

| Reviewer | Rec | Sig | Meth | Val | Clar | Eth | Scope | Avg |
|----------|-----|-----|------|-----|------|-----|-------|-----|
| Claude   | Major | 4 | 2 | 2 | 3 | 3 | 3 | 2.8 |
| Gemini   | Major | 4 | 3 | 3 | 5 | 4 | 4 | 3.8 |
| GPT-5.2  | Major | 4 | 2 | 2 | 3 | 3 | 3 | 2.8 |
| **Avg**  |       | 4.0 | 2.3 | 2.3 | 3.7 | 3.3 | 3.3 | **3.1** |

## Blocking Items (All 3 reviewers)

### 1. Transport model is under-specified and possibly double-counted (All 3)
- **Problem:** Model samples both `transport_cost_per_kg` and `delta_v`/`Isp`/`payload_fraction` independently. But transport cost IS a function of delta-v and Isp — sampling both independently creates inconsistency and potential double-counting.
- **Solution:** Derive transport_cost_per_kg FROM delta_v, Isp, and vehicle economics rather than sampling it independently. Use the Tsiolkovsky equation properly. Add fleet sizing model (number of vehicles, trip time, utilization rate).
- **Files:** `water_extraction_model.py`, LaTeX §3.3

### 2. EP transfer time not modeled — time value of water (All 3)
- **Problem:** Low-thrust EP transfers from NEAs take months-years. The model ignores transit time, meaning water tied up in transit is a hidden cost. Lunar water arrives much faster.
- **Solution:** Add trip time calculation based on delta-v and thrust/mass ratio. Model water-in-transit as working capital cost. This may narrow the NEA-lunar cost gap.
- **Files:** `water_extraction_model.py`, LaTeX §3

### 3. Bennu extrapolation to general NEA population (Claude, GPT)
- **Problem:** Paper uses Bennu (one asteroid) to characterize all C-type NEAs. Compositional heterogeneity within and between C-type NEAs is not addressed.
- **Solution:** Add paragraph on spectral type diversity within C-types (CI, CM, CR, etc.). Use meteorite database to establish population-level water fraction distribution. Widen MC range if needed.
- **Files:** LaTeX §2.1

### 4. Correlated parameters not modeled (Claude, GPT)
- **Problem:** Water fraction and extraction yield may be positively correlated (more water → easier extraction). Independent sampling overstates uncertainty.
- **Solution:** Add correlation structure to MC (rank correlation matrix). Test sensitivity to correlation assumptions.
- **Files:** `water_extraction_mc.py`, LaTeX §4

### 5. No sensitivity/tornado analysis (GPT)
- **Problem:** Paper reports MC distributions but doesn't identify which parameters drive the most uncertainty.
- **Solution:** Add Spearman rank correlation analysis (already exists in Paper 01's MC engine — reuse). Present tornado chart of parameter importance.
- **Files:** `water_extraction_mc.py`, LaTeX §5 (new subsection)

## Optional Improvements

- Add Hayabusa2/Ryugu data as second calibration point (Gemini)
- Model non-water co-products (metals, organics) as cost offsets (Claude)
- Address extraction technology maturity (TRL) for each source (GPT)
- Add comparison with Earth-launched water cost as reference line (GPT)
