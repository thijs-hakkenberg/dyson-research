---
paper: "02-swarm-coordination-scaling"
version: "cl"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-03-03"
recommendation: "Unknown"
---



# Peer Review: Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms

## 1. Significance & Novelty
**Rating: 3 (Adequate)**

The paper addresses a genuine gap: closed-form parametric sizing for hierarchical coordination at the $10^3$–$10^5$ node scale with byte-level traffic accounting. The two-layer feasibility framework (byte budget + TDMA airtime) is a useful conceptual contribution, and the generalized $\gamma$ expression (Eq. 12) is genuinely practical. However, the novelty is tempered by the fact that the individual components—TDMA slot analysis, GE channel modeling, M/D/1 queueing, AoI analysis—are well-established. The contribution is primarily one of *integration and parameterization* rather than fundamental methodological advance. The absence of any external validation limits the significance claim: the framework produces internally consistent design estimates, but its predictive utility for real systems remains undemonstrated.

## 2. Methodological Soundness
**Rating: 3 (Adequate)**

The analytical framework is internally consistent, and the multi-tool approach (analytical equations, cycle-aggregated DES, slot-level simulator, packet-level simulator) provides useful cross-checks. However, several methodological concerns arise:

- The DES operates at message-layer granularity and confirms its own equations by construction (acknowledged by the authors). The claimed <0.1% agreement is verification, not validation—this is correctly stated but the incremental value of the DES beyond distributional tails is modest.
- The slot-level simulator reveals the ARQ×TDMA coupling (52.7% deadline misses), which is a genuinely useful finding invisible to the fluid-server DES. This is the strongest methodological contribution.
- The GE channel parameterization is acknowledged as illustrative, but the paper's quantitative conclusions (e.g., "P95 = 4 cycles") are presented with a specificity that may mislead readers into treating them as calibrated predictions rather than parametric examples.
- The static topology assumption is reasonable for bandwidth sizing but limits applicability to dynamic constellations where cluster churn is non-negligible.

## 3. Validity & Logic
**Rating: 4 (Good)**

The logical structure is sound. The paper carefully distinguishes between Model S (simplified) and Model C (CCSDS-grounded), and all feasibility claims use Model C. The campaign duty factor $d$ is a well-motivated addition that properly contextualizes the stress-case $\eta_S \approx 46\%$ as a continuous-duty upper bound rather than a typical operating point. The three-tier overhead decomposition (baseline/architecture-specific/workload-dependent) is clean and consistently applied.

The gamma unification around 0.76 (replacing the earlier 0.85) appears consistently applied throughout—Tables III, V, VII, VIII, and the rate ladder (Table IV) all reference Model C values. The generalized $\gamma$ expression (Eq. 12) correctly captures the rate dependence ($\gamma_{24} = 0.761$, $\gamma_{30} = 0.745$).

One logical tension: the paper argues that 1 kbps is the design-driving regime (RF-backup, <1% of lifetime), yet devotes the majority of analysis to this regime. While justified for worst-case sizing, the practical relevance of the TDMA analysis is limited to a narrow operational window. This is acknowledged but could be more prominently framed.

## 4. Clarity & Structure
**Rating: 3 (Adequate)**

The paper is comprehensive but dense. At its current length, it reads more like a technical report than a journal article. The roadmap paragraph at the start of Section IV is helpful, but the reader must navigate numerous cross-references, footnotes, and conditional statements. Specific concerns:

- Table I (notation) is useful but incomplete—some symbols appear in equations before being defined in text.
- The proliferation of tables (13+) and figures (8+) is excessive for a journal paper; several could be consolidated or moved to supplementary material.
- The distinction between "screening heuristic" and "design criterion" (Section IV, feasibility workflow) is stated but may confuse practitioners who want a single go/no-go test.
- Algorithm 1 is a valuable synthesis but appears late in the paper (Section V-C); moving it earlier or providing a forward reference would improve readability.
- Some notation is overloaded: $\gamma$ appears with various subscripts ($\gamma_S$, $\gamma_C$, $\gamma_{24}$, $\gamma_{30}$, $\gamma_{\min}$) that are not always disambiguated at point of use.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**

The paper is exemplary in its transparency. The AI disclosure is specific (tools named, scope of use delineated). Data availability is comprehensive (GitHub tag, environment specification, runtime estimates). The validation gap is prominently acknowledged in multiple locations (abstract, Section V-A, Table X, conclusion). The claim map (Table X) is an unusually honest and useful artifact. The authors do not overclaim.

## 6. Scope & Referencing
**Rating: 4 (Good)**

The literature coverage is broad, spanning constellation management, swarm robotics, distributed systems, queueing theory, AoI, and CCSDS standards. The DVB-RCS2 reference is a welcome addition for TDMA context. The Lutz et al. and ITU-R P.681 references appropriately ground the GE model. Minor gaps: no reference to recent work on LEO ISL measurement campaigns (e.g., Starlink laser ISL characterization efforts), and the network calculus mention (Le Boudec) is acknowledged but not developed. The paper is appropriate for IEEE T-AES in scope, though the length exceeds typical journal articles.

---

## Major Issues

1. **The DES provides limited independent validation beyond distributional tails.**
   - *Issue:* The DES confirms analytical means to <0.1% by construction (same equations). The authors acknowledge this (Tier 1 verification) but still present DES results prominently throughout. The distributional tail analysis (Fig. 6, bimodal coordinator ingress) is the DES's genuine contribution, but this could be obtained analytically via MMPP/D/1 tail bounds (acknowledged as future work).
   - *Why it matters:* Readers may overestimate the validation depth. The paper has four tools that all implement the same model—agreement is necessary but not sufficient for confidence.
   - *Remedy:* Reduce DES presentation to the distributional findings. Add a paragraph explicitly stating: "DES-analytical agreement verifies implementation correctness; it does not validate the underlying model assumptions (message sizes, arrival rates, GE parameters)." Consider deriving at least approximate MMPP/D/1 tail bounds to replace the DES for this purpose.

2. **No pathway to external validation is concretely specified.**
   - *Issue:* The paper repeatedly states "external validation is future work" and "no ISL-specific GE measurements exist," but provides no concrete plan for how validation would be conducted, what data would be needed, or what agreement thresholds would confirm or refute the framework.
   - *Why it matters:* Without a validation roadmap, the framework remains an internally consistent but untested design tool. For a journal of record, the gap between "preliminary design estimates" and actionable engineering guidance needs a clearer bridge.
   - *Remedy:* Add a subsection (or expand Section V-A) specifying: (a) what ISL channel measurements are needed (minimum: $p_{BG}$, $p_B$, coherence time statistics for 2–3 obstruction mechanisms); (b) what NS-3 simulation would test (MAC contention, antenna scheduling, multi-cluster interference); (c) quantitative acceptance criteria (e.g., "if measured $\gamma$ differs by >10% from Eq. 12, the rate ladder shifts by one step"). This transforms the limitation from a disclaimer into a research agenda.

3. **The packet-level validation (Section IV-J) anchors $\gamma$ but does not independently validate the sizing framework.**
   - *Issue:* The packet-level simulator derives $\gamma$ from CCSDS framing parameters—this is parameter anchoring, not model validation. The sizing equations themselves ($\eta$, coordinator ingress, AoI) are not tested against an independent model or data source.
   - *Why it matters:* The claim map (Table X) correctly labels this as "Anchoring" rather than "Tier 2," but the section title ("Standards-Grounded Parameter Derivation") and the prominence given to cross-model consistency may give readers a false sense of validation depth.
   - *Remedy:* Retitle Section IV-J to "Physical-Layer Parameter Anchoring" or similar. Add a sentence: "This derivation validates the $\gamma$ parameter value, not the sizing equations that consume it." Consider whether a comparison against DVB-RCS2 TDMA efficiency measurements (publicly available) could provide partial external anchoring.

4. **The stress-case contextualization, while improved, still risks misinterpretation.**
   - *Issue:* The campaign duty factor $d$ is well-motivated, and Table VII with worked examples is helpful. However, the abstract still leads with "$\eta_0 \approx 5\%$" without immediately contextualizing that the stress-case $\eta_S \approx 46\%$ is episodic. The 46% figure appears in Table II (first results table) without the $d$ context.
   - *Why it matters:* A reader scanning the abstract and Table II will see "46% overhead" and may dismiss the framework as impractical before reaching the duty-factor analysis in Section IV-E.
   - *Remedy:* In the abstract, add "routine operations yield $\eta \approx 5$–$10\%$" (already present—good) but also add "(stress-case $\eta_S \approx 46\%$ is a continuous-duty upper bound, episodic in practice)." In Table II, add a row or footnote showing $\eta$ at $d = 0.10$.

5. **The three-layer claim is actually two layers plus a screening heuristic.**
   - *Issue:* The paper sometimes refers to a "three-layer feasibility framework" (title area of review prompt) but the actual framework is two layers (byte budget + TDMA airtime) plus a non-binding screening heuristic ($\eta_{\text{total}}/\gamma < 0.50$). The coordinator capacity sizing is derived from Layer 2, not a separate layer.
   - *Why it matters:* Overcounting layers inflates the perceived complexity and contribution.
   - *Remedy:* Consistently describe the framework as two-layer throughout. The screening heuristic is useful but should be clearly labeled as a convenience, not a third layer. (The paper mostly does this already—ensure consistency.)

## Minor Issues

1. **Eq. 12 units:** The $10^{-3}$ conversion factor in Eq. 12 is error-prone. Consider expressing guard and acquisition in seconds (matching $R_{\text{PHY}}$ in bps) to eliminate the conversion factor, or add a dimensional analysis note.

2. **Table I:** $\alpha_{\text{RX}}$ is defined as "0.908 at $k_c = 100$, 30 kbps Model C" but this is a derived quantity, not a parameter. Clarify that it is computed from the schedule, not an input.

3. **Section III-B-2:** "Each cluster coordinator sends a single 512-byte summary per cycle (vs. forwarding $k_c$ individual reports)"—this aggregation ratio should be justified. What information is lost? Is 512 B sufficient for a meaningful cluster summary of 100 nodes?

4. **GE parameter table (Table III):** $p_{GB} = 0.05$/cycle and $p_{BG} = 0.50$/cycle yield steady-state availability $\pi_G = p_{BG}/(p_{BG}+p_{GB}) = 0.909$. State this explicitly for readers unfamiliar with GE models.

5. **Fig. 4 (cross-cycle recovery):** The DES validation points (squares) in panel (b) appear at only three $p_{BG}$ values. Adding 1–2 more points (e.g., $p_{BG} = 0.30, 0.70$) would strengthen the visual validation.

6. **Algorithm 1, Line 10:** $L_{\text{cmd}}$ uses "egress window directly" but the comment should reference the specific equation for traceability.

7. **Section III-C (Node Model):** "5 W baseline power (15–20 W coordinator mode)"—the power model is mentioned but never used in any analysis. Either develop its implications (e.g., for coordinator rotation scheduling) or remove it.

8. **Typo/style:** "Eq.~\ref{eq:gamma_derived}" in Section IV-A is referenced before the equation appears in the text flow for a first-time reader (it appears in the same section but the forward reference in the slot-timing model box at the start of Section I may confuse).

9. **Reference [1] (Starlink):** The FCC filing is appropriate, but the "Jonathan's Space Report" citation is non-archival and should be removed or replaced with a peer-reviewed source.

10. **Table X (Claim Map):** The "Pkt-$\gamma$" column header with the $\ddagger$ footnote is hard to parse. Consider "CCSDS $\gamma$ anchoring" as the column header.

11. **Section V-B (Limitations):** "correlated modes are future work"—given that the GE model explicitly handles temporal correlation, clarify that this refers to *spatial* correlation (common-cause failures affecting multiple nodes/clusters simultaneously).

---

## Overall Recommendation
**Recommendation: Major Revision**

This is a substantial and carefully constructed paper that addresses a real gap in the literature: parametric sizing equations for hierarchical coordination in large autonomous space swarms. The two-layer feasibility framework is conceptually sound, the CCSDS-grounded $\gamma$ derivation is practically useful, and the campaign duty factor elegantly resolves the earlier concern about stress-case realism. The claim map (Table X) and the explicit acknowledgment of the validation gap set a commendable standard for intellectual honesty.

However, the paper suffers from three interrelated weaknesses that prevent acceptance in its current form. First, the validation architecture is circular: four tools implementing the same equations confirm each other, with the genuine incremental findings (ARQ×TDMA coupling, distributional tails) occupying a small fraction of the analysis. The paper needs to more sharply distinguish verification from validation and reduce the prominence of DES-analytical agreement. Second, the absence of any external validation pathway—even a concrete specification of what data or simulation would be needed—limits the paper's utility as engineering guidance. Third, the paper's length and density exceed what is appropriate for a journal article; consolidation of tables and figures, with supplementary material for detailed parameter sweeps, would significantly improve readability.

The strongest elements—the generalized $\gamma$ expression, the rate ladder, Algorithm 1, and the GE sensitivity sweep—should be preserved and elevated. With focused revision addressing the validation roadmap, presentation density, and the DES's role, this paper would make a solid contribution to IEEE T-AES.

## Constructive Suggestions

1. **Highest impact:** Add a concrete validation roadmap (Section V-A extension) specifying required ISL measurements, NS-3 simulation scope, and quantitative acceptance criteria. This transforms the limitation into a research contribution.

2. **High impact:** Reduce paper length by 20–25%. Move Tables V, VI, IX to supplementary material. Consolidate the GE mechanism table (Table VI) with the sensitivity sweep discussion. Trim the DES presentation to distributional findings only.

3. **High impact:** Elevate Algorithm 1 to Section IV (after the feasibility workflow definition) and provide a worked numerical example walking through all steps for the default parameter set. This is the paper's most actionable output for practitioners.

4. **Medium impact:** Add a DVB-RCS2 TDMA efficiency comparison as partial external anchoring for $\gamma$. Published DVB-RCS2 slot efficiencies (0.70–0.85 depending on burst length) would provide an independent sanity check.

5. **Medium impact:** Derive approximate MMPP/D/1 tail bounds (even if only for the dominant eigenvalue approximation) to provide analytical backing for the DES distributional findings, reducing dependence on simulation for the paper's most novel DES contribution.

6. **Medium impact:** Add a "quick-start" summary table mapping common mission profiles (LEO constellation, deep-space swarm, GEO cluster) to recommended parameter sets ($k_c$, $T_c$, $R_{\text{PHY}}$, $d$), making the framework immediately usable.

7. **Lower impact:** Provide the generalized $\gamma$ expression as a downloadable calculator (already partially addressed via GitHub) with a web interface for practitioners who will not clone a repository.