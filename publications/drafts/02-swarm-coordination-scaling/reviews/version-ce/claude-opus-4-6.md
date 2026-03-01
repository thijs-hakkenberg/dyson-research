---
paper: "02-swarm-coordination-scaling"
version: "ce"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-28"
recommendation: "Unknown"
---



# Peer Review: "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms"

---

## 1. Significance & Novelty
**Rating: 3 (Adequate)**

The paper addresses a genuine gap: no prior work provides closed-form parametric sizing relationships for hierarchical coordination at the $10^3$–$10^5$ node scale with byte-level traffic accounting. The two-layer feasibility framework (byte budget + TDMA airtime) and the decomposition into topology-dependent ($\eta_0$) and workload-dependent ($\eta_{\text{cmd}}$) components are useful organizational contributions. However, the novelty is tempered by several factors: (1) the individual analytical components (M/D/1 queueing, GE channel models, AoI geometric analysis, TDMA slot budgeting) are well-established; the contribution is their assembly, not new theory; (2) the "design equations" are essentially dimensional analysis and bookkeeping—valuable for practitioners but modest in intellectual depth; (3) the paper's scope is narrower than the title suggests, as it addresses only the message/MAC layer under a specific set of assumptions, with the most interesting physical-layer interactions deferred to future NS-3 work.

## 2. Methodological Soundness
**Rating: 3 (Adequate)**

The three-layer verification approach (DES, slot-level simulator, packet-level simulator) is well-structured and the IEEE 1012 verification taxonomy is a welcome framing. However, several methodological concerns arise:

- The DES is cycle-aggregated and message-layer only; its agreement with closed-form equations is "expected by construction" (the authors' own words). The distributional analysis (Fig. 7) provides some added value but is limited.
- The slot-level TDMA simulator and packet-level simulator are described but their implementations are not independently validated against any external benchmark or existing tool.
- The GE channel model parameters are acknowledged as illustrative, which is appropriate, but the sensitivity analysis covers only two dimensions ($p_{BG}$, $p_B$) while holding $p_{GB}$ fixed at 0.05—a significant limitation given that the steady-state bad-state probability $\pi_B = p_{GB}/(p_{GB}+p_{BG})$ is jointly determined.
- The Monte Carlo configuration (30 replications) is adequate for mean estimation given the reported SD < 0.001%, but the tail statistics (P99 AoI, P95 GE recovery) would benefit from more replications or importance sampling, particularly since the paper makes specific claims about rare events.

## 3. Validity & Logic
**Rating: 4 (Good)**

The internal logic is generally sound and the paper is careful about stating assumptions. Several specific strengths:

- The campaign duty factor $d$ now adequately addresses workload realism. The stress-case ($\eta_S \approx 46\%$) is properly contextualized as a continuous-duty upper bound ($d=1$), with realistic operations at $d = 0.01$–$0.10$ yielding $\eta \approx 5$–$10\%$. The worked campaign scenarios (orbit-raising, station-keeping, collision avoidance) are helpful anchors.
- The $\gamma = 0.76$ derivation from CCSDS Proximity-1 framing (replacing the earlier 0.85) is consistently applied throughout the paper—I verified this in Tables IV, V, VII, VIII, IX, and the design equations summary. This is a significant improvement.
- The three-layer feasibility framework is logically sound: Layer 1 (byte budget) is necessary but not sufficient; Layer 2 (TDMA airtime) is the decisive schedulability test; coordinator capacity closes the loop. Table VI correctly shows that stress unicast passes Layer 1 but fails Layer 2.
- The distinction between broadcast (Type 1) and unicast (Type 2) commands, with the stagger equation (Eq. 12), is a useful practical insight.

However, some logical gaps remain:

- The claim that command traffic is "topology-invariant" is qualified as holding "given the assumed workload semantics (centralized command generation)," but this qualification is easy to miss. The paper itself shows that Raft consensus yields $\eta_{\text{consensus}} \approx 30.7\%$, which is *not* topology-invariant. This undermines the generality claim.
- The coordinator failure analysis assumes independent failures, but the paper acknowledges correlated failures are unmodeled. For a system designed around coordinator availability, this is a significant gap.

## 4. Clarity & Structure
**Rating: 4 (Good)**

The paper is well-organized with a clear roadmap at the beginning of Section IV. The notation table (Table I) is helpful, and the canonical overhead definitions (Section III-F) impose useful discipline. The tool scope disambiguation paragraph is valuable.

However, the paper is extremely dense—it reads more like a technical report than a journal article. At approximately 12,000 words of body text plus extensive tables and figures, it pushes the limits of what a reader can absorb. Some specific issues:

- The paper oscillates between the 1 kbps RF-backup regime (which drives the TDMA analysis) and higher-rate regimes where everything is trivially feasible. This creates cognitive overhead as the reader must constantly track which regime is under discussion.
- Several results are stated multiple times in slightly different forms (e.g., the 30 kbps design point appears in at least six locations).
- The verification taxonomy, while thorough, makes it difficult to identify what is genuinely *new* knowledge versus confirmation of known equations.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**

The data availability statement is exemplary: source code, configuration files, MC datasets, all simulators, and link budget calculator are provided at a tagged repository. The AI disclosure is present and appropriately scoped. The paper is transparent about what is modeled and what is not (Table XII). Author anonymization is noted as pending final publication.

## 6. Scope & Referencing
**Rating: 3 (Adequate)**

The reference list (55 items) covers the major relevant areas but has notable gaps:

- No references to actual ISL hardware demonstrations or measurements (e.g., EDRS, LCRD, Starlink ISL characterization papers).
- The network calculus reference (Le Boudec) is cited but not used; the paper would benefit from actually comparing its worst-case bounds to network calculus service curves.
- Missing references to recent work on distributed TDMA scheduling in satellite networks (e.g., work by Radhakrishnan et al. on ISL MAC protocols).
- The CCSDS references are appropriate but the paper does not cite CCSDS 401.0 (Earth Stations and Spacecraft) for the link budget parameters.
- Several references are non-archival (Amazon, DARPA, DoD websites); while understandable, this weakens the scholarly foundation.

---

## Major Issues

**1. The DES provides limited independent validation beyond confirming its own equations.**

The authors acknowledge this ("expected by construction") and position the DES's value as distributional analysis. However, the distributional contribution (Fig. 7, bimodal ingress CDF) is a single figure showing an unsurprising result: stochastic ON/OFF campaigns produce bimodal load. This does not justify the extensive DES infrastructure described. The paper would be stronger if it either (a) demonstrated a non-obvious emergent behavior discovered through DES that the closed-form misses, or (b) reduced the DES discussion to a brief verification note and devoted the space to the more interesting slot-level and packet-level analyses.

*Remedy:* Either strengthen the DES contribution with additional distributional insights (e.g., joint AoI × buffer occupancy distributions, transient behavior during coordinator handoff, correlated failure cascades) or significantly condense the DES description and results.

**2. The packet-level validation (Section IV-J) derives γ from standards but does not validate the *system-level* sizing equations against an independent physical-layer model.**

The packet-level simulator computes γ from CCSDS framing parameters—this is valuable but is essentially a more careful version of Eq. (6). It does not simulate actual packet-level behavior (contention, capture effects, timing jitter distributions, multi-path). The "cross-model verification" (Table XI) shows four models agreeing because they all implement the same equations with the same γ. This is consistency, not validation.

*Remedy:* (a) Clearly label Section IV-J as "standards-grounded parameter derivation" rather than "validation." (b) Discuss what a true packet-level validation would require (NS-3 with realistic ISL channel models, multi-cluster interference). (c) Consider whether the γ decomposition (Eq. 7, Table VII) could be validated against published CCSDS Proximity-1 throughput measurements if any exist.

**3. The generalized γ expression (Eq. 19) conflates bit-domain and time-domain quantities in a way that may confuse practitioners.**

The denominator mixes coded bits ($[S \times 8 + O_{\text{frame}}]/R_{\text{FEC}}$) with time-domain quantities converted to bits ($(T_{\text{guard}} + T_{\text{acq}}) \times R_{\text{PHY}} \times 10^{-3}$). While dimensionally correct, this formulation obscures the physical meaning. A practitioner unfamiliar with the derivation might incorrectly apply it (e.g., using information-rate rather than PHY-rate for $R_{\text{PHY}}$, or confusing pre-FEC and post-FEC bit counts).

*Remedy:* Present the equation in time-domain form (ratio of payload transmission time to total slot time), which is more intuitive and less error-prone. Provide a worked numerical example alongside the equation.

**4. The static topology assumption limits the applicability of the AoI and GE recovery results.**

The paper assumes fixed cluster membership for one year. While the J2 perturbation analysis (Section V-B) shows low re-association rates for Walker constellations, many practical swarm scenarios involve non-Walker geometries, formation reconfiguration, or phasing maneuvers where cluster membership changes frequently. The AoI and GE recovery analyses assume a stable coordinator-member relationship; during re-association, both metrics would degrade in ways not captured by the 0.3% byte-budget overhead estimate.

*Remedy:* (a) Bound the AoI transient during cluster re-association analytically (not just the 33 s estimate). (b) Discuss how GE recovery statistics change when the channel state is reset upon re-association. (c) Identify the re-association rate threshold above which the static assumption breaks down.

**5. The paper lacks a clear comparison with any existing operational or proposed system.**

The centralized and global-state mesh baselines are intentional bounds, not realistic alternatives. No comparison is made with, e.g., Starlink's actual coordination overhead, Iridium's ISL management protocol, or any proposed autonomous constellation management scheme. This makes it difficult to assess whether the framework produces results that are consistent with operational experience.

*Remedy:* Include at least one calibration point against published operational data (even if approximate). For example, Starlink's ground-based conjunction screening cadence could be mapped to an equivalent $p_{\text{exc}}$ and $T_c$ to check whether the AoI framework produces reasonable numbers.

---

## Minor Issues

1. **Table I notation:** $\alpha_{\text{RX}}$ is defined as "ingress fraction of $T_c$ (0.918 at $k_c = 100$)" but the superframe budget (Table V) shows ingress = 9,177 ms out of 10,000 ms = 0.9177, and total allocated = 9,377 ms. Clarify whether $\alpha_{\text{RX}}$ includes or excludes the sync beacon.

2. **Eq. (2):** The hierarchy equation $M_{\text{total}} = N + N/k_c + N/(k_c \cdot k_r)$ counts upward messages only. Downward commands, heartbeats, and summaries are described in text but not in the equation. Consider a complete bidirectional message count equation.

3. **Section III-C (Node Model):** "5 W baseline power (15–20 W coordinator mode)" is stated without justification. What drives the 3–4× power increase for coordinators? Is this the radio or the processing?

4. **Table III:** The collision avoidance rate ($10^{-4}$/node/s) is described as "screening notifications" in the footnote, but the message size (128 B) and the term "collision avoidance" suggest autonomous alerts. Clarify the operational concept.

5. **Fig. 1:** The architecture diagram is referenced but the figure content is not visible in this review. Ensure it clearly shows the four levels with fan-out ratios and message flow directions.

6. **Section IV-A:** "Phase-staggered scheduling ($\phi_j = (j/n_{\text{clusters}}) \times T_c$)" assumes global synchronization of cluster phases. How is this achieved without a centralized scheduler? This seems to contradict the autonomous coordination premise.

7. **Eq. (14):** The AoI P99 formula uses $\lceil \cdot \rceil$ (ceiling), which is correct for discrete cycles, but the DES reports 441 s while the formula gives 440 s. The 1 s difference is within one $T_c$ step but should be noted as a discretization artifact, not measurement error.

8. **Table IX (Link Availability):** The footnote states "$M_r = 2$ columns apply to Regime A only" but the table header does not distinguish regimes. Consider splitting into two sub-tables or adding regime labels to column headers.

9. **Section IV-E:** "Commands account for >60% of stress-case traffic" — this should be stated more precisely. From Table II: 410/870 = 47% of total per-node traffic, or 410/670 = 61% of overhead traffic. Clarify the denominator.

10. **References:** [1] cites an FCC filing and a non-archival website in the same entry. Split into two references. [3] and [4] are non-archival; provide DOIs or archival alternatives where possible.

11. **Eq. (19):** The $10^{-3}$ unit conversion factor is fragile. Consider using consistent SI units throughout or defining a helper variable $T_{\text{overhead}} = T_{\text{guard}} + T_{\text{acq}}$ in seconds.

12. **Section V-B:** "J2 perturbation analysis (Walker constellation: 53°, 550 km, 72 planes × 22 sats)" — this specific constellation is never introduced earlier. State whether this is Starlink-like and cite the orbital parameters source.

---

## Overall Recommendation
**Recommendation: Major Revision**

This paper makes a useful contribution by assembling a complete sizing procedure for hierarchical coordination in large spacecraft swarms, from message-layer byte budgets through TDMA schedulability to coordinator capacity requirements. The two-layer feasibility framework is well-conceived, the campaign duty factor $d$ appropriately contextualizes the stress-case, and the standards-grounded γ = 0.76 derivation from CCSDS Proximity-1 is a meaningful improvement over assumed values. The data availability and reproducibility provisions are exemplary.

However, the paper suffers from a validation gap that it acknowledges but does not adequately mitigate. The DES confirms its own equations; the packet-level simulator derives a parameter rather than validating system behavior; and no comparison with operational data is provided. The result is a self-consistent analytical framework whose correspondence to physical reality remains undemonstrated. The paper is also excessively long for the depth of new insight it provides—much of the content is careful bookkeeping rather than new science.

For major revision, the authors should: (1) sharpen the distinction between consistency checks and genuine validation, reducing the DES discussion and strengthening the packet-level analysis; (2) provide at least one calibration point against operational or experimental data; (3) address the static topology limitation more rigorously; (4) condense the presentation by approximately 20%, eliminating redundant restatements of key results; and (5) clarify the generalized γ expression for practitioner use.

## Constructive Suggestions

1. **Highest impact:** Add a calibration against operational data. Even a rough comparison (e.g., "Starlink's reported conjunction screening cadence of X events/day across Y satellites implies an effective $p_{\text{exc}} \approx Z$, yielding AoI consistent with our framework") would significantly strengthen the paper's credibility.

2. **High impact:** Restructure the verification narrative. Currently, four tools are presented as providing "independent" verification, but they share the same equations. Reframe: the analytical equations are the primary contribution; the DES provides distributional extensions; the slot-sim reveals ARQ×TDMA coupling (a genuine insight not in the equations); the packet-level tool anchors γ. This honest framing is more compelling than the current presentation.

3. **High impact:** Condense Sections IV-F and IV-G. The scaling invariance of η with N is trivially expected from the equations (η depends on $k_c$ and message sizes, not N). The topology comparison adds little beyond what Table X already shows. These sections could be reduced to a single paragraph each with supporting figures moved to an appendix.

4. **Medium impact:** Extend the GE sensitivity analysis to sweep $p_{GB}$ jointly with $p_{BG}$, or at minimum show how the steady-state availability $\pi_G = p_{BG}/(p_{BG}+p_{GB})$ maps to the design curves. Currently, fixing $p_{GB} = 0.05$ while sweeping $p_{BG}$ conflates two effects (burst duration and burst frequency).

5. **Medium impact:** Add a "quick-start" design procedure box or flowchart that walks a practitioner through the sizing equations step by step, with decision points (e.g., "Is $\eta_{\text{total}}/\gamma < 0.5$? If yes, CSMA suffices; if no, proceed to TDMA sizing"). This would significantly increase the paper's practical utility.

6. **Lower impact:** Consider whether the sectorized mesh (Section III-B.4) adds sufficient value to justify its inclusion. It is described as "functionally distinct" from the hierarchical architecture and appears only in one figure and one table. If retained, its role as a local-monitoring reference should be more clearly motivated.