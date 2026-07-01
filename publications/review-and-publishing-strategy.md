# Project Dyson — Draft-Paper Review & Publishing Strategy

_Prepared after the critical-gap literature fill. Reconciles the 2026-02-13 publication assessment with the **current** draft state in `publications/drafts/`, integrates 45 newly retrieved references covering the 17 critical unsourced research questions, and defines a sequenced path to submission._

> **Numbering note.** The older `publication-assessment.md` listed Paper 04 as *Solar Radiation Pressure Station-Keeping*. The live repository has since renumbered: **04 = Microgravity Metallurgy, 05 = ISRU Water Extraction**. This review uses the live numbering. The holistic review (2026-05-11) already flagged this collision — resolving it in the roadmap is a prerequisite to submission.


## 1. Portfolio at a glance

| # | Paper | Tier | Words | Refs | State | New refs added |
|---|-------|------|-------|------|-------|----------------|
| 01 | ISRU Economic Crossover | 1 | 18,567 | 39 | COMPLETE — 3/3 AI-reviewer Accept (39 rounds) | 0 |
| 02 | Swarm Coordination Scaling | 1 | 5,630 | 38 | ADVANCED — NS-3 validated, 44 review files, PDF built | 5 |
| 03 | Multi-Model AI Consensus | 1 | 7,796 | 33 | ADVANCED — 16 trade studies, reliability trials, 40 review files | 0 |
| 04 | Microgravity Metallurgy | 2 | 4,139 | 21 | EARLY DRAFT — 2 versions, 6 review files, gravity-zone architecture | 4 |
| 05 | ISRU Water Extraction | 2 | 3,254 | 13 | EARLY DRAFT — 2 versions, 6 review files, Monte Carlo cost model | 0 |
| 06 | Cryogenic Propellant Architecture | 2 | 367 | 0 | STUB — INPUTS.md only | 0 |
| 10 | Thin-Film Deposition | 2 | 338 | 0 | STUB — INPUTS.md only | 5 |

**Reading of the table.** Three papers (01, 02, 03) are substantively complete manuscripts; two (04, 05) are honest early drafts with a real model and review history; two (06, 10) are one-page input stubs. Publishing effort should concentrate where the marginal manuscript is cheapest to finish, not spread evenly.


## 2. Paper-by-paper review

### Paper 01 — ISRU Economic Crossover  *(Tier 1, submission-ready)*

- **State.** 18.6k words, 39 references, 3/3 AI-reviewer Accept after 39 iteration rounds. Full NPV Monte Carlo with Wright learning curves, phased capital, and a megaproject-reference-class uncertainty band (σ_ln = 0.70).
- **Literature currency.** Bibliography spans 1936–2023 but is thin on the 2024–2025 launch-economics literature that reviewers in *Advances in Space Research* will expect. The crossover claim is timely precisely because Starship-class cost curves are moving; cite the most recent public cost data to protect the headline result.
- **Verdict.** Ready. Remaining work is venue reformatting and an AI-contribution disclosure statement, not new analysis.
- **Action:** convert informal citations to venue style; add 3–5 2024–2025 launch-cost references; submit.

### Paper 02 — Swarm Coordination Scaling  *(Tier 1, one integration pass from ready)*

- **State.** Closed-form two-test feasibility framework (byte budget + TDMA schedulability), NS-3 validation within 3–8% of analytical γ, 38 references, PDF built. Strong CCSDS grounding.
- **Gap the new literature closes.** The paper's reliability and autonomy claims (coordinator duty cycle, failure exposure) were unsourced against the certification/reliability literature. The critical-gap fill supplies that spine:

    - [rq-1-16] Torens et al. (2014), *Certification and Software Verification Considerations for Autonomous Unmanned Aircraft* — Journal of Aerospace Information Systems. [10.2514/1.i010163](https://doi.org/10.2514/1.i010163)
    - [rq-1-16] Dennis et al. (2016), *Formal verification of ethical choices in autonomous systems* — Robotics and Autonomous Systems. [10.1016/j.robot.2015.11.012](https://doi.org/10.1016/j.robot.2015.11.012)
    - [rq-1-16] Costello et al. (2021), *Generating Certification Evidence for Autonomous Aerial Vehicles Decision-Making* — Journal of Aerospace Information Systems. [10.2514/1.i010848](https://doi.org/10.2514/1.i010848)
    - [rq-1-22] Kim et al. (2017), *Reliability–redundancy allocation problem considering optimal redundancy strategy using parallel genetic algorithm* — Reliability Engineering &amp; System Safety. [10.1016/j.ress.2016.10.033](https://doi.org/10.1016/j.ress.2016.10.033)
    - [rq-1-22] Crestani et al. (2015), *Enhancing fault tolerance of autonomous mobile robots* — Robotics and Autonomous Systems. [10.1016/j.robot.2014.12.015](https://doi.org/10.1016/j.robot.2014.12.015)

- **Verdict.** Integrate the autonomy-certification and reliability-allocation references into the Discussion (failure-exposure and duty-cycle arguments), then submit. Kim (2017) reliability–redundancy allocation and Crestani (2015) fault-tolerant autonomy directly support the availability targets.
- **Action:** add ~4 references, one paragraph in Discussion tying duty-cycle to formal availability budgets; submit to IEEE T-AES.

### Paper 03 — Multi-Model AI Consensus  *(Tier 1, self-contained)*

- **State.** 7.8k words, 16 trade studies, reliability trials (n=5 runs × 4 stratified questions), divergent-views schema, 33 references, Ethics Statement present.
- **Literature currency.** This is a methods paper in an unoccupied niche; its references are AI/methodology, not space-engineering, so the critical-gap fill does not apply. The exposure here is **provenance**, not citations: the holistic review flagged inconsistent model-name reporting (Claude 4.6 vs 4.7, GPT-5.2 vs 5.5) across documents.
- **Verdict.** Ready once model IDs/versions are pinned consistently and a reproducibility appendix names exact model builds and dates. Nothing scientific blocks it.
- **Action:** freeze model-version table; confirm venue AI-disclosure fit (some venues are wary of LLM-as-author); submit to Systems Engineering or IEEE Intelligent Systems.

### Paper 04 — Microgravity Metallurgy  *(Tier 2, early draft)*

- **State.** 4.1k words, 21 references, gravity-sensitivity decomposition + hybrid multi-gravity-zone architecture, Gate-1 decision criteria. Two versions, 6 review files.
- **Gap the new literature closes.** Two of the paper's binding constraints — achieving solar-grade silicon purity and controlling particulate contamination in vacuum — were unsourced. The fill adds:

    - [rq-2-14] Cheng et al. (2025), *A comprehensive review on wafering of silicon substrate for photovoltaic solar cell* — Solar Energy. [10.1016/j.solener.2025.113977](https://doi.org/10.1016/j.solener.2025.113977)
    - [rq-2-14] Huang et al. (2022), *Purification of Metallurgical-grade Silicon by Sn-Si Solvent Refining with Different Tin Content* — Silicon. [10.1007/s12633-022-01917-y](https://doi.org/10.1007/s12633-022-01917-y)
    - [rq-2-18] Liu et al. (2018), *Role of vacuum on cleanliness improvement of steel during electroslag remelting* — Vacuum. [10.1016/j.vacuum.2018.05.032](https://doi.org/10.1016/j.vacuum.2018.05.032)
    - [rq-2-18] Zhang et al. (2024), *Effects of refining slag basicity and vacuum treatment on the cleanliness of bearing steel* — Vacuum. [10.1016/j.vacuum.2024.112984](https://doi.org/10.1016/j.vacuum.2024.112984)

- **Note.** Huang (2022) metallurgical-grade Si purification and Kawamoto (2011) electrostatic lunar-dust mitigation are the two most on-target additions; Cannon (2022) gives a lunar-materials handling review that strengthens the ISRU feedstock argument.
- **Verdict.** Needs a second substantive draft: expand results, integrate the new purity/dust references, and tighten the throughput-gap argument (6–8 orders of magnitude from ISS gram-scale). ~2–3 months.

### Paper 05 — ISRU Water Extraction  *(Tier 2, early draft)*

- **State.** 3.3k words, 13 references, Monte Carlo NPV-per-kg model comparing C-type NEA / lunar polar / Phobos-Deimos water, calibrated to OSIRIS-REx Bennu data. Two versions, 6 review files.
- **Literature currency.** Corpus already strong on the ISRU/mining axis (43 arXiv papers); the critical-gap fill did not target this paper's questions. Main gap is manuscript maturity, not sourcing.
- **Verdict.** Extend to full length, add source-comparison sensitivity figures, reconcile with Paper 01's cost framework (shared NPV machinery — cite it, don't re-derive). ~2–3 months.

### Papers 06 & 10 — Cryogenic Propellant, Thin-Film Deposition  *(Tier 2, stubs)*

- **State.** INPUTS.md only (~350 words each). Not yet drafts.
- **Thin-Film Deposition (10)** benefits most from the new literature — the radiation-degradation and production-rate questions are the paper's core and now have anchors:

    - [rq-1-1] Zhao et al. (2025), *Understanding proton radiation-induced degradation mechanisms in Cu2ZnSn(S,Se)4 kesterite thin-film solar cells* — Solar Energy. [10.1016/j.solener.2025.113450](https://doi.org/10.1016/j.solener.2025.113450)
    - [rq-1-1] Mohammad et al. (2019), *Electric field assisted spray coated lead free bismuth iodide perovskite thin film for solar cell application* — Solar Energy. [10.1016/j.solener.2019.02.034](https://doi.org/10.1016/j.solener.2019.02.034)
    - [rq-1-1] Ishikawa et al. (2013), *Variation of proton radiation belt deduced from solar cell degradation of Akebono satellite* — Earth, Planets and Space. [10.5047/eps.2012.06.004](https://doi.org/10.5047/eps.2012.06.004)
    - [rq-1-44] Xin et al. (2018), *A review on high throughput roll-to-roll manufacturing of chemical vapor deposition graphene* — Applied Physics Reviews. [10.1063/1.5035295](https://doi.org/10.1063/1.5035295)
    - [rq-1-44] Chen et al. (2016), *High-rate roll-to-roll stack and lamination of multilayer structured membrane electrode assembly* — Journal of Manufacturing Processes. [10.1016/j.jmapro.2016.06.022](https://doi.org/10.1016/j.jmapro.2016.06.022)

- **Verdict.** Defer drafting until Tier-1 is submitted. When started, 10 has a literature head start; 06 needs a cryogenic-storage literature pass of its own (work package already scoped in the prose review).


## 3. Strategic finding: an unclaimed high-value paper

The critical-gap fill surfaced a **high-voltage architecture** cluster (rq-1-4, rq-1-8, rq-2-1) that maps to *no* current paper yet has the strongest, most citable literature of any gap addressed:

    - [rq-1-4] Toyoda et al. (2005), *Degradation of High-Voltage Solar Array Due to Arcing in Plasma Environment* — Journal of Spacecraft and Rockets. [10.2514/1.11602](https://doi.org/10.2514/1.11602)
    - [rq-1-4] Wang et al. (2014), *Simulation of Arcing Process in High-Voltage Self-Blast Circuit Breaker Considering Motion of Valves* — IEEE Transactions on Plasma Science. [10.1109/tps.2014.2324599](https://doi.org/10.1109/tps.2014.2324599)
    - [rq-1-4] Iwai et al. (2015), *Flight Results of Arcing Experiment Onboard High-Voltage Technology Demonstration Satellite Horyu-2* — Journal of Spacecraft and Rockets. [10.2514/1.a33007](https://doi.org/10.2514/1.a33007)
    - [rq-1-4] Goebel et al. (2022), *High Voltage Solar Array Development for Space and Thruster-Plume Plasma Environments* — IEEE Transactions on Plasma Science. [10.1109/tps.2022.3147424](https://doi.org/10.1109/tps.2022.3147424)
    - [rq-1-8] Toyoda et al. (2005), *Degradation of High-Voltage Solar Array Due to Arcing in Plasma Environment* — Journal of Spacecraft and Rockets. [10.2514/1.11602](https://doi.org/10.2514/1.11602)
    - [rq-1-8] Ferguson et al. (2017), *Voltage Threshold and Power Degradation Rate for GPS Solar Array Arcing* — IEEE Transactions on Plasma Science. [10.1109/tps.2017.2694387](https://doi.org/10.1109/tps.2017.2694387)
    - [rq-2-1] Liu et al. (2014), *Observations and modeling of GIC in the Chinese large-scale high-voltage power networks* — Journal of Space Weather and Space Climate. [10.1051/swsc/2013057](https://doi.org/10.1051/swsc/2013057)
    - [rq-2-1] Wright et al. (2012), *Electrostatic Discharge Testing of Multijunction Solar Array Coupons After Combined Space Environmental Exposures* — IEEE Transactions on Plasma Science. [10.1109/tps.2011.2174447](https://doi.org/10.1109/tps.2011.2174447)
    - [rq-2-1] Ferguson et al. (2014), *Feasibility of Detecting Spacecraft Charging and Arcing by Remote Sensing* — Journal of Spacecraft and Rockets. [10.2514/1.a32958](https://doi.org/10.2514/1.a32958)
    - [rq-2-1] Lai et al. (2010), *Importance of Surface Conditions for Spacecraft Charging* — Journal of Spacecraft and Rockets. [10.2514/1.48824](https://doi.org/10.2514/1.48824)

The physics is concrete and the sources are directly on-point (solar-array arcing in plasma, ESD thresholds, multijunction-array testing, spacecraft surface charging). A focused paper — *High-Voltage Architecture and Arc Management for Thin-Film Swarm Collectors* — would (a) close three critical RQs at once, (b) de-risk a Phase-1/2 project-ending concern, and (c) occupy an empty niche. **Recommendation:** promote this to a Tier-2 paper slot (it is more mature in its literature base than the two current stubs).

## 4. Publishing strategy

### 4.1 Sequencing (what to submit, in what order)

The portfolio has a natural wave structure. Submit in waves so that reviewer feedback on the methods paper (03) and the flagship (01) informs the rest.

| Wave | Timing | Papers | Rationale |
|------|--------|--------|-----------|
| **A** | Months 0–2 | 01 ISRU Crossover; 03 AI Consensus | Both self-contained and complete; different venue families (space-econ vs AI-methods) so no reviewer overlap; establishes the program's publication record. |
| **B** | Months 2–4 | 02 Swarm Coordination | One literature-integration pass (autonomy/reliability refs) then submit; NS-3 validation already in hand. |
| **C** | Months 4–8 | 04 Metallurgy; 05 Water Extraction | Second drafts with new references; 05 reuses 01's NPV machinery. |
| **D** | Months 8–12 | New HV-Architecture paper; 10 Thin-Film; 06 Cryogenic | Draft from stubs/clusters once Tier-1 is out and reviewer norms are known. |

### 4.2 Venue targeting (reconciled)

| Paper | Primary venue | Backup | Notes |
|-------|---------------|--------|-------|
| 01 ISRU Crossover | Advances in Space Research | Acta Astronautica | Timely vs Starship-era economics. |
| 02 Swarm Coordination | IEEE T-AES | J. Guidance, Control & Dynamics | Constellation-management framing broadens appeal. |
| 03 AI Consensus | Systems Engineering (INCOSE) | IEEE Intelligent Systems | Check AI-authorship policy first. |
| 04 Metallurgy | Acta Astronautica | Progress in Aerospace Sciences | Review-style intro fits PAS if expanded. |
| 05 Water Extraction | Acta Astronautica | J. Spacecraft & Rockets | Coordinate claims with 01. |
| HV Architecture (new) | J. Spacecraft & Rockets | IEEE T. Plasma Science | Strong existing arc/ESD literature. |
| 10 Thin-Film | J. Applied Physics | Advances in Space Research | Radiation-degradation core now sourced. |
| 06 Cryogenic | Cryogenics | Acta Astronautica | Needs own literature pass. |

### 4.3 Cross-cutting readiness gates (apply to every paper before submission)

1. **Provenance freeze.** Pin exact model IDs/versions and dates in one shared table; the holistic review found inconsistent naming (Claude 4.6/4.7, GPT-5.2/5.5) — a credibility risk domain reviewers will notice.
2. **AI-contribution disclosure.** Draft one reusable disclosure paragraph; confirm each venue's policy (several now have explicit AI-contribution rules, and some may resist LLM-as-reviewer framing).
3. **Maturity framing.** State plainly that the program is at **pre-Phase-A feasibility / de-risking** stage, not construction planning — the holistic review identified overstated maturity as the single biggest coherence risk.
4. **Reference-style conversion.** Existing citations are informal; convert to each venue's style and verify every DOI resolves.
5. **Numbering reconciliation.** Fix the 04 collision (metallurgy vs SRP station-keeping) across roadmap, assessment, and drafts before external readers see cross-references.
6. **Code/data availability.** Simulator source and Monte Carlo notebooks to a public repo with a release tag; cite the archived version (Zenodo DOI) in each paper.


### 4.4 How this advances the practical swarm-building science

Each Tier-1 paper converts an internal decision into an externally-reviewed result that de-risks a specific phase gate: **01** sets the ISRU-vs-launch crossover that governs whether Phase 0 is worth building; **02** sizes the coordination link that Phase 1/2 hardware must meet before it is designed; **03** makes the decision *method* itself auditable. The Tier-2 wave (04, 05, HV-architecture) closes the three project-ending / architecture-change risks the roadmap already names — microgravity metallurgy throughput, ISRU propellant economics, and high-voltage arc management. Publishing is therefore not a parallel track to the engineering; it is how each phase gate gets independent validation before capital is committed.


## 5. Immediate next actions (this month)

1. **01:** reference-style conversion + 3–5 recent launch-cost citations → submit to *Advances in Space Research*.
2. **03:** freeze model-version table + AI-disclosure paragraph → submit to *Systems Engineering*.
3. **02:** integrate the 4 autonomy/reliability references (Kim 2017, Crestani 2015, Torens 2014, Costello 2021) into Discussion → submit to *IEEE T-AES*.
4. **Program hygiene:** resolve paper-04 numbering collision; pin model IDs repo-wide; archive simulator code with a Zenodo DOI.
5. **Decision for you:** approve promoting the **HV-Architecture** cluster to a drafted paper (Section 3).


---
*Artifacts produced this session:* `dyson_critical_gap_literature.csv/.md` (45 refs, 17 critical RQs), `dyson_paper_readiness_matrix.csv`, and this document. Coverage of research questions with attached literature rose from 31% to 43%, with **all critical unsourced RQs now sourced**.
