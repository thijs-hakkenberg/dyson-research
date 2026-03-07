---
paper: "02-swarm-coordination-scaling"
version: "dn"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-03-07"
recommendation: "Unknown"
---

## Peer Review: "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms" (Version DN)

---

## 1. Significance & Novelty
**Rating: 3 (Adequate)**

The paper addresses a genuine gap: closed-form parametric sizing for hierarchical coordination in large autonomous spacecraft swarms with byte-level traffic accounting. The two-test feasibility framework (byte budget + TDMA airtime) is a useful conceptual contribution, and the campaign duty factor $d$ is a practical parameterization. However, the novelty is incremental rather than transformative. The core analytical machinery—TDMA slot efficiency calculations, M/D/1-style queueing, Gilbert-Elliott channel modeling—is well-established. The primary contribution is assembling these known techniques into a coherent sizing methodology for a specific (and currently hypothetical) application domain. The paper would benefit from a clearer articulation of what is genuinely new versus what is engineering integration of existing tools. The $10^4$–$10^5$ node regime claimed as underexplored is true for autonomous coordination, but the paper's results are fundamentally per-cluster ($k_c = 50$–$500$), and the fleet-level scaling analysis (spatial reuse, Eq. 16) is admittedly provisional.

## 2. Methodological Soundness
**Rating: 3 (Adequate)**

The analytical framework is internally consistent and carefully constructed. The three-layer decomposition (byte budget → MAC efficiency → TDMA airtime) is logically sound, and the rate ladder (Table V) provides a clear audit trail. However, several methodological concerns persist:

- The cycle-aggregated DES is acknowledged to reproduce analytical means to <0.1%, which raises the question of its independent value. The authors correctly note this confirms implementation, not model validity—but this means the DES contributes little beyond a code check.
- The NS-3 validation is the strongest methodological element, but the "matched-assumptions" experiment that narrows discrepancy to <2% is somewhat circular: it validates the model under its own assumptions rather than testing those assumptions against reality.
- The GE channel parameterization is grounded in Lutz et al. for land-mobile satellite channels, but ISL channels have fundamentally different propagation characteristics. The authors acknowledge this ("ISL structural shadowing is expected to be less severe"), but this undermines the quantitative GE results.
- The spatial reuse factor $R = 7$ is acknowledged as provisional, yet fleet-level feasibility depends critically on it.

## 3. Validity & Logic
**Rating: 4 (Good)**

The internal logic is generally tight. The decomposition of $\eta$ into baseline, architecture-specific, and workload-dependent components is clean and well-motivated. The campaign duty factor $d$ effectively addresses earlier concerns about workload realism—Table III provides concrete mission-phase mappings that make the stress-case ($\eta_S \sim 46\%$) clearly contextualized as a continuous-duty upper bound occurring <1% of operational time. This is a significant improvement.

The $\gamma$ unification around 0.73–0.76 (CCSDS-validated) is consistently applied throughout. Model S ($\gamma = 0.949$) is clearly flagged as "not for design." The sensitivity analysis (Eq. 8) quantifying the impact of $\Delta\gamma$ on $R_{\text{PHY,min}}$ is useful.

One logical concern: the feasibility threshold derivation (§III-A) assumes independent per-cycle delivery for the geometric tail argument, then immediately notes that GE correlation violates this assumption. The transition between these regimes could be more rigorous—currently it reads as two separate analyses rather than a unified treatment.

## 4. Clarity & Structure
**Rating: 4 (Good)**

The paper is well-organized and generally well-written. The notation table (Table I) is comprehensive. The rate ladder (Table V) is an excellent pedagogical device. Algorithm 1 provides a clear synthesis. The abstract is informative and accurately represents the content.

Areas for improvement: the paper is dense, and the relationship between the many tables could be streamlined. Some redundancy exists between the text and tables (e.g., the 20.2 kbps figure appears in at least four places). The Discussion section mixes validation interpretation with limitation acknowledgment in a way that could be better structured.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**

The AI disclosure is specific and appropriate (tools named with version numbers, scope of use clearly delineated). Data availability is exemplary—code, NS-3 scenarios, datasets, and configuration are provided with a specific repository tag. The paper is transparent about what the DES does and does not validate. Reproducibility appears excellent.

## 6. Scope & Referencing
**Rating: 3 (Adequate)**

The reference list covers the major relevant areas (CCSDS standards, DVB-RCS2, swarm robotics, DTN, constellation management). However, several gaps exist:

- No reference to the substantial body of work on TDMA scheduling optimization for satellite networks (e.g., Choi & Shin on real-time TDMA, or the extensive DVB-S2/RCS literature beyond the single ETSI standard cited).
- The Age of Information literature is cited but not deeply engaged—recent work on AoI under correlated channels (directly relevant to the GE model) is absent.
- No engagement with the growing literature on federated satellite systems or distributed satellite computing architectures.
- The LEACH comparison is somewhat superficial; more recent cluster-head protocols (HEED, TEEN) address energy-aware scheduling that may be relevant.

---

## Major Issues

**1. The DES provides negligible independent validation value.**
- *Issue:* The DES reproduces analytical means to <0.1% by construction (same equations, same assumptions). The authors acknowledge this but still present it as part of the V&V framework.
- *Why it matters:* Readers may overestimate the degree of independent validation. The DES confirms code correctness, not model validity.
- *Remedy:* Either (a) reduce the DES to a brief implementation-verification note (1–2 sentences) and elevate the NS-3 validation and slot-level simulator as the primary validation tools, or (b) use the DES for something the analytical model cannot do—e.g., transient analysis, rare-event statistics, or correlated failure scenarios that break the mean-value assumptions.

**2. The NS-3 "matched-assumptions" experiment validates assumptions against themselves.**
- *Issue:* The matched-assumptions run enforces the same framing and deterministic acquisition as the analytical model, then shows <2% agreement. This confirms that the analytical model is self-consistent, not that its assumptions are realistic.
- *Why it matters:* The more informative result is the 3–8% discrepancy in the "realism run," which reveals the cost of the analytical abstractions. The matched-assumptions experiment, while useful for decomposing the gap, should not be presented as the primary validation result.
- *Remedy:* Restructure §IV-B to lead with the realism-run results and the feasibility-boundary agreement (both models agree on 24 kbps infeasible, 35 kbps feasible). Present the matched-assumptions experiment as a diagnostic tool for understanding the gap, not as the validation headline. Also, acknowledge that the NS-3 model itself uses idealized assumptions (star topology, no Doppler, no orbital dynamics) that limit its claim to "independent" validation.

**3. GE channel parameters lack ISL-specific justification.**
- *Issue:* The GE parameters are drawn from Lutz et al. (1991), which characterizes land-mobile satellite channels at L/S-band with terrain shadowing. ISL channels experience fundamentally different impairments (structural shadowing from spacecraft body, solar interference, but no terrain multipath).
- *Why it matters:* The quantitative GE results (27.1% intra-cycle recovery, P95 = 4 cycles) are presented with specificity that implies more grounding than exists. The Discussion paragraph on channel-model grounding acknowledges this but does not adequately propagate the uncertainty into the quantitative claims.
- *Remedy:* (a) Add explicit uncertainty bounds on the GE-derived metrics (e.g., "under the assumed GE parameters; actual ISL channels may differ by an order of magnitude in $p_B$"). (b) Provide $\gamma$ and recovery metrics for a wider range of GE parameters (partially done in Fig. 5b, but not for the slot-level results). (c) Consider adding a simple ISL-specific channel argument (e.g., structural shadowing duty cycle from body geometry) to bound $p_B$ for ISL.

**4. Fleet-level feasibility depends on unvalidated spatial reuse.**
- *Issue:* Eq. 16 and the surrounding analysis assume $R = 7$ spatial reuse, acknowledged as "provisional pending RF simulation." At $R = 1$, fleet-level TDMA is infeasible ($G = 25$). At $R = 3$, latency doubles.
- *Why it matters:* The paper's title and abstract imply applicability to "large autonomous space swarms," but the per-cluster results only scale to fleet level if spatial reuse is sufficient. This is a critical assumption that is entirely unvalidated.
- *Remedy:* (a) Add a more prominent caveat in the abstract and conclusion that fleet-level results are conditional on spatial reuse validation. (b) Provide a simple geometric argument for minimum achievable $R$ given directional S-band antenna patterns and typical orbital separations. (c) Consider whether the paper should be explicitly scoped as "per-cluster sizing" rather than implying fleet-level applicability.

**5. The generalized $\gamma$ expression (Eq. 7) needs practitioner guidance on parameter selection.**
- *Issue:* Eq. 7 is presented as useful for practitioners, but the component timing values ($T_{\text{guard}}$, $T_{\text{acq}}$, $O_{\text{frame}}$) require hardware-specific knowledge that practitioners may not have at the preliminary design stage.
- *Why it matters:* The paper's stated goal is preliminary design sizing. If practitioners cannot populate Eq. 7 without hardware selection, its utility is limited.
- *Remedy:* Provide a table of recommended $\gamma$ ranges for common radio classes (COTS S-band, custom ISL, UHF backup) with references to representative hardware datasheets. The alternative slot structures (Table VII) partially address this but could be more explicitly framed as a practitioner lookup table.

## Minor Issues

1. **Abstract length:** At ~200 words, the abstract is dense but within IEEE limits. However, the phrase "cold-start timing is the most conservative assumption" appears without context and may confuse readers unfamiliar with the slot structure analysis.

2. **Table II, Panel A:** The column header "100 kbps" in the bandwidth regime section shows $\eta_{\text{total,stress}} = 0.66\%$, but this should be verified—at 100 kbps, the stress-case overhead should be $\eta_0 + 1.0 \times 0.41\% + 20.5\% \approx 21\%$, not 0.66%. The scaling $\eta \propto 1/C_{\text{node}}$ applies to $\eta$, not $\eta_{\text{total}}$. Please verify or clarify.

3. **Eq. 14 (AoI):** The geometric inter-report assumption is stated parenthetically but deserves more justification. If exception reports are triggered by threshold crossings on correlated state variables, the geometric model may significantly underestimate tail AoI.

4. **Table VI, "GE exc." column:** The header is cryptic. Please expand to "GE + exception reporting" or similar.

5. **§II-D:** "Runtime: ~7 s at $N = 10^5$" — specify hardware (CPU, RAM) for reproducibility.

6. **Fig. 1:** Referenced but described only as a PDF. The caption should describe the fan-out parameters more precisely (e.g., "default: $k_r = 10$, $k_c = 100$").

7. **Eq. 12 (fleet reuse):** $f_{\text{RF}}$ is introduced without definition. From context it appears to be the fraction of nodes requiring RF coordination simultaneously, but this should be explicit.

8. **§III-A, feasibility threshold derivation:** The bound "$\epsilon^{50} < 0.01$ is satisfied for any $\epsilon < 0.91$" is trivially true and not informative. The binding constraint analysis that follows is more useful—consider removing the non-binding bound.

9. **Reference [12]:** Self-citation to a non-peer-reviewed technical report on "multi-model AI deliberation." This is appropriate for the AI disclosure but should not be counted as a substantive reference.

10. **Supplement references:** Multiple results are deferred to supplementary sections (§§B, C, D, F, G, H, I, L, M). While appropriate for space constraints, the main text should be self-contained for the core claims. Verify that no critical derivation step is only in the supplement.

11. **Typo/style:** "Coord. bottleneck?" in Table II uses a superscript "c" footnote marker that could be confused with the variable $c$ in queueing notation.

12. **§V, "Falsification conditions":** Condition (iv) states that measured $\tau_c \ll T_c$ with $p_B < 0.3$ would make 35 kbps "unnecessary"—this is not a falsification but rather a relaxation. Rephrase to distinguish conditions that invalidate the recommendation from those that relax it.

---

## Overall Recommendation
**Recommendation: Major Revision**

This paper makes a useful engineering contribution by assembling a coherent parametric sizing framework for hierarchical coordination in large spacecraft swarms. The two-test feasibility decomposition is clean, the campaign duty factor effectively addresses workload realism, and the CCSDS-grounded $\gamma$ analysis is carefully executed. The NS-3 validation and alternative slot structure analysis are welcome additions that strengthen the paper relative to what earlier versions likely contained.

However, several substantive issues prevent acceptance in the current form. The validation strategy, while improved, still relies heavily on self-consistency checks (DES reproducing its own equations, matched-assumptions NS-3 confirming the model under its own assumptions). The GE channel parameters lack ISL-specific grounding, and the fleet-level feasibility claim depends on unvalidated spatial reuse. The paper's scope oscillates between "per-cluster preliminary design" (which is well-supported) and "large autonomous space swarms" (which requires fleet-level validation that is absent).

The most impactful revision would be to (1) sharpen the scope to per-cluster sizing with explicit fleet-level caveats, (2) restructure the validation narrative to lead with the NS-3 realism-run results and feasibility-boundary agreement rather than the matched-assumptions self-consistency, and (3) provide ISL-specific channel parameter bounds or at minimum propagate the GE parameter uncertainty into the quantitative claims. The analytical framework itself is sound and, with these revisions, would represent a solid contribution to the preliminary design literature for large constellation coordination.

## Constructive Suggestions

1. **Highest impact:** Restructure the validation narrative. Lead with "both models agree on the feasibility boundary" as the headline result. Demote the DES to an implementation check. Present the NS-3 realism run as the primary validation and the matched-assumptions run as diagnostic.

2. **High impact:** Scope the paper explicitly as per-cluster sizing. Move fleet-level analysis to a clearly marked "extension" subsection with prominent caveats. Adjust the title if necessary (e.g., "Per-Cluster Design Equations...").

3. **High impact:** Provide ISL-specific channel parameter bounds. Even a simple geometric shadowing analysis (spacecraft body subtends X degrees, solar exclusion zone Y degrees) would ground the GE parameters far better than the Lutz land-mobile reference.

4. **Medium impact:** Add a practitioner-oriented $\gamma$ lookup table spanning common radio hardware classes, with conservative/nominal/optimistic values and source references.

5. **Medium impact:** Use the DES for something the analytical model cannot do—rare-event analysis, correlated failure cascades, or transient behavior during cluster re-formation. This would justify its inclusion as more than a code check.

6. **Medium impact:** Engage more deeply with the AoI literature under correlated channels. The GE model creates exactly the correlation structure that recent AoI papers address; connecting to this literature would strengthen both the analytical framework and the reference list.

7. **Lower impact:** Provide a sensitivity table showing how the key recommendations ($R_{\text{PHY}} = 35$ kbps, $k_c = 100$) change under simultaneous variation of the three most uncertain parameters ($T_{\text{acq}}$, $\gamma$, $p_B$). A 3D feasibility surface or contour plot would be more informative than the current one-at-a-time sensitivity analyses.