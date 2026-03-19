# Revision Plan: Paper 04 Version B

## Review Summary (Version A)

| Reviewer | Rec | Sig | Meth | Val | Clar | Eth | Scope | Avg |
|----------|-----|-----|------|-----|------|-----|-------|-----|
| Claude   | Major | 4 | 2 | 3 | 4 | 3 | 2 | 3.0 |
| Gemini   | Major | 4 | 3 | 4 | 5 | 2 | 3 | 3.5 |
| GPT-5.2  | Major | 4 | 2 | 3 | 4 | 4 | 3 | 3.3 |
| **Avg**  |       | 4.0 | 2.3 | 3.3 | 4.3 | 3.0 | 2.7 | **3.3** |

## Blocking Items (All 3 reviewers)

### 1. Gravity sensitivity thresholds need quantitative support (Claude #1, Gemini, GPT #1)
- **Problem:** Stokes law extrapolation to partial gravity without accounting for non-Newtonian rheology, turbulence, droplet polydispersity. Grashof number argument is necessary but insufficient.
- **Solution:** Add parametric analysis with realistic ranges; cite Ratke's slag separation data; add caveats about single-droplet vs. emulsion behavior; frame thresholds as "order-of-magnitude guidance requiring experimental validation."
- **Files:** LaTeX §3

### 2. Reference list far too thin (Claude #6, Gemini, GPT)
- **Problem:** Only 11 references for a "systematic literature review." Missing NASA/ESA microgravity materials science, rotating station design, ISRU processing literature. Uncited references [8-11] in bibliography.
- **Solution:** Add 20-30 references: ISS EML experiments, Dold & Benz FZ silicon, Spacelab/USML metallurgy, NASA Nautilus-X, FFC Cambridge process, Hall/Globus rotating stations, specific NASA TMs from external research.
- **Files:** LaTeX bibliography

### 3. Mass estimates need basis of estimate (Claude #2, GPT #1)
- **Problem:** 340,000-430,000 kg stated without mass breakdown structure or subsystem estimates. "±30% uncertainty" likely optimistic.
- **Solution:** Add a mass breakdown table with subsystem-level estimates. Reference ISS module masses and existing station concept studies for calibration.
- **Files:** LaTeX §4, new Table

### 4. AI methodology transparency (Gemini #1)
- **Problem:** AI-assisted methodology relies on "in preparation" reference [1]. Boundary between AI and human content unclear.
- **Solution:** Add a methodology subsection describing the multi-model deliberation process. Add data availability statement. Clarify AI vs. human contributions explicitly.
- **Files:** LaTeX §1 or new §1.1

### 5. Electrolysis section disconnected (Claude, GPT)
- **Problem:** §2.4 on microgravity electrolysis feels bolted onto a metallurgy paper.
- **Solution:** Either integrate it into the processing chain narrative (electrolysis produces H2/O2 needed for certain metallurgical processes) or move to a brief mention with reference.
- **Files:** LaTeX §2.4

## Optional Improvements

- TRL assignments should be reviewed for consistency (Claude)
- Contingency reduction argument is premature (Claude) — add temporal qualifier
- Add Coriolis force quantitative analysis for melt pools (GPT)
- Cost projection methodology for the $550-810M roadmap (GPT)
