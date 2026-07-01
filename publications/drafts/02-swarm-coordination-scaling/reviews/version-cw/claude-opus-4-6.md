---
paper: "02-swarm-coordination-scaling"
version: "cw"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-03-05"
recommendation: "Unknown"
---



# Peer Review: "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms"

---

## 1. Significance & Novelty
**Rating: 3 (Adequate)**

The paper addresses a genuine gap: no prior work provides closed-form parametric sizing relationships for hierarchical coordination architectures at the $10^3$–$10^5$ node scale with byte-level traffic accounting. The two-layer feasibility framework (byte budget + TDMA airtime) and the actionable Algorithm 1 are useful contributions for preliminary mission design. However, the novelty is tempered by several factors: (1) the core analytical results are relatively straightforward traffic accounting and scheduling arithmetic rather than deep theoretical contributions; (2) the absence of any external validation means the practical utility remains speculative; and (3) the paper's scope is explicitly limited to "loose coordination" via S-band RF, with tight formation control deferred to optical ISL—narrowing the applicability. The generalized $\gamma$ expression (Eq. 7) is genuinely useful for practitioners, providing a clean parameterization that accommodates diverse link technologies. The campaign duty factor $d$ is a sensible and well-motivated addition that substantially improves workload realism.

## 2. Methodological Soundness
**Rating: 3 (Adequate)**

The three-layer feasibility framework (byte budget, MAC efficiency, TDMA airtime) is logically structured, and the paper is commendably transparent about what each layer does and does not capture. The analytical equations are correctly derived and internally consistent. However, several methodological concerns arise:

- The DES verification is largely tautological—confirming its own equations to <0.1%—and the paper acknowledges this honestly (Tier 1 verification only). The distributional tail analysis (Fig. 4) is the DES's genuine incremental contribution, but it depends entirely on the assumed ON/OFF Markov campaign process, which is itself unvalidated.
- The GE channel model is appropriately labeled as a "what-if design tool," but the default parameterization ($p_{BG} = 0.50$, $p_B = 0.90$) is not grounded in any ISL measurement. The sensitivity sweeps (Fig. 3b) partially mitigate this, but the paper's specific numeric claims (e.g., "27% intra-cycle recovery") are artifacts of the assumed coherence model.
- The slot-level simulator and the packet-level $\gamma$ derivation share the same equation set (Eq. 7), so their agreement is by construction. The paper correctly notes this but could be clearer about what "cross-model anchoring" actually provides beyond parameter consistency checking.
- The $M/D/1$ centralized baseline and global-state mesh are intentionally simplified reference bounds, not competing architectures—this is appropriate but limits the comparative value of the topology analysis.

## 3. Validity & Logic
**Rating: 4 (Good)**

The internal logic is generally sound and self-consistent. The paper has clearly undergone significant revision to address prior concerns:

- The campaign duty factor $d$ now properly contextualizes the stress-case ($\eta_S \approx 46\%$) as a continuous-duty upper bound that is episodic in practice ($<$1% of operational time). Table VII maps mission phases to duty factors with empirical anchoring (ESA CA maneuver rates). This is a substantial improvement.
- The gamma unification around CCSDS Proximity-1 framing ($\gamma_{30} = 0.745$, replacing an earlier 0.85) is consistently applied throughout. I verified spot-checks: Table VI, the rate ladder (Table IV), Algorithm 1, and the feasibility summary (Table V) all use Model C values. The Model S values appear only where explicitly labeled (Table VIII, Fig. 5).
- The parameter dependency map (Section IV preamble) correctly separates ingress-side constraints (independent of $d$, $q$) from egress/byte-budget concerns. The "100% deadline misses at 24 kbps" is correctly identified as an ingress constraint.
- The rate paradox ($\gamma$ decreasing with $R_{\text{PHY}}$) is correctly explained and consistently handled.

One logical concern: the paper claims $\alpha_{\text{RX}}$ is "derived from the schedule, not an external input" (Algorithm 1, line 6), but then uses $\alpha_{\text{RX}} = 0.908$ as if it were a fixed parameter in several places. This is technically correct (it is derived at 30 kbps) but could confuse readers who don't track the rate-dependence carefully.

## 4. Clarity & Structure
**Rating: 3 (Adequate)**

The paper is dense but generally well-organized. The roadmap at the beginning of Section IV is helpful, and the notation table (Table I) is comprehensive. However:

- The paper is extremely long for a journal article and suffers from over-documentation. Many caveats, cross-references, and footnotes—while individually justified—collectively impede readability. The reader must track two slot-timing models, three overhead tiers, two feasibility tests, a design heuristic, and numerous rate definitions across 30+ equations.
- The repeated warnings ("do not apply the heuristic AND Test B independently," "Model S is NOT for design," etc.) suggest the framework is more confusing than it needs to be. A cleaner separation—perhaps relegating Model S entirely to an appendix—would help.
- Table II (Parameter Sensitivity Summary) appears before the methodology is fully explained, which is disorienting.
- The figures are referenced but not shown in the manuscript text (as expected for a review draft). The descriptions suggest they are appropriate.
- Algorithm 1 is a genuine strength—it synthesizes the entire framework into an actionable procedure.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**

The paper is exemplary in its transparency: code and data are publicly available with a tagged release; AI usage is disclosed with specific model versions; the validation gap is prominently acknowledged (abstract, Section V-A, conclusion); the GE model is repeatedly labeled as a "what-if design tool"; and the claim map (Table IX) explicitly categorizes every result by evidence tier. This level of intellectual honesty is commendable and should be a model for the field.

## 6. Scope & Referencing
**Rating: 3 (Adequate)**

The literature coverage is broad, spanning constellation management, swarm robotics, distributed systems theory, queueing theory, and CCSDS standards. Key references (LEACH, Raft, AoI framework, network calculus, GE channel models) are appropriately cited. However:

- The paper does not engage with recent work on distributed satellite computing architectures (e.g., Denby & Lucia, "Orbital Edge Computing," IEEE Micro 2020) or on-orbit task scheduling that would provide relevant context.
- The DVB-RCS2 reference is used for $\gamma$ uncertainty bounding, but the analogy between ground terminal return links and ISL TDMA is acknowledged as imperfect. More ISL-specific references (even from CubeSat missions with S-band ISL demonstrations) would strengthen the grounding.
- Several references are non-archival (Amazon Kuiper overview, DARPA program pages, DOD fact sheets). While understandable for programmatic context, these weaken the scholarly foundation.
- The self-citation to the "multi-model AI deliberation" tech report [55] is of questionable relevance.

---

## Major Issues

**1. The DES provides minimal independent validation beyond confirming its own equations.**

The paper honestly acknowledges this (Tier 1 verification), but the DES still occupies substantial manuscript real estate. The distributional tail analysis (Fig. 4, Section IV-F) is the sole non-tautological DES contribution, yet it depends entirely on the assumed ON/OFF Markov campaign process. The buffer sizing rule ($M = 1.30$ at $d = 0.10$) is labeled "not model-robust"—appropriately—but this undermines its practical value.

*Why it matters:* Readers may overestimate the validation status of the framework. The DES creates an illusion of independent confirmation where none exists.

*Remedy:* Either (a) substantially reduce the DES presentation to a brief verification note and the distributional figure, or (b) add a genuinely independent validation element. The most accessible option would be an NS-3 simulation of even a simplified TDMA scenario (e.g., 10 nodes, single cluster) to validate the $\gamma$-based abstraction against a full MAC/PHY stack. If this is infeasible for the current submission, the DES sections should be compressed and the paper should be more concise about what the DES adds.

**2. The packet-level validation (Section IV-J) does not provide independent validation of the framework.**

The $\gamma$ derivation from CCSDS Proximity-1 framing is a standards-based parameter estimate, not a measurement. The paper correctly states this, but Section IV-J is titled "Standards-Based Slot Efficiency Parameterization"—which is accurate—yet it is listed as "Tier 2: Cross-model anchoring" in Table IX. Since the packet-level simulator and the analytical equations share Eq. 7, their agreement is definitional. The DVB-RCS2 comparison ($\gamma = 0.70$–$0.85$) provides a useful plausibility check but is from a different domain (ground terminals, not ISLs).

*Why it matters:* The distinction between parameter estimation and validation is critical for practitioners who will rely on these design equations.

*Remedy:* Relabel Section IV-J's contribution as "parameter anchoring" (which the paper already does in places) consistently throughout, including in Table IX. Remove or downgrade the "Tier 2" label for CCSDS $\gamma$; it is parameter estimation, not cross-model validation. Explicitly state that no Tier 2 validation exists for the overall framework (only for the ARQ×TDMA coupling via the slot simulator, which is a genuine cross-model finding).

**3. Fleet-level scaling claims are insufficiently supported.**

The spatial reuse argument (Eq. 6, $R = 3$, $F = 4$) is described as an "order-of-magnitude plausibility argument," but the paper still makes fleet-level claims ($N = 10^5$) in the abstract and throughout. The 20 dB isolation assumption at 500 km with 6 dBi antennas needs more justification—sidelobe levels, near-far effects, and dynamic geometry could substantially reduce effective reuse. The paper acknowledges this in Section V-C but continues to use $10^5$ as a headline number.

*Why it matters:* The title promises "large autonomous space swarms," but the validated scope is per-cluster ($k_c = 50$–$500$). Fleet-level claims without NS-3 or equivalent validation risk misleading mission designers.

*Remedy:* Either (a) add a substantive fleet-level analysis (interference geometry, realistic antenna patterns, dynamic reuse scheduling) or (b) restrict all claims to per-cluster scope and modify the title/abstract accordingly. At minimum, add a brief interference calculation showing the sensitivity of $R$ to antenna sidelobe levels and orbital geometry.

**4. The 1 kbps per-node budget justification is circular in places.**

The paper states that 1 kbps is a "baseline design target" and provides a physical justification (200 kbps aggregate / 100 nodes × $\gamma$ = ~1.5 kbps, with 50% margin). However, the 200 kbps aggregate itself depends on the link budget at a specific range, power, and antenna gain that are stated but not derived from mission requirements. The paper then shows that at ≥10 kbps, all constraints are trivially satisfied—which raises the question of why the 1 kbps regime is the focus.

*Why it matters:* If the 1 kbps budget is the binding constraint that makes the entire TDMA analysis necessary, its justification must be airtight. The paper's own results show that modest increases (to 2–10 kbps) eliminate all feasibility concerns.

*Remedy:* Provide a more rigorous link budget derivation showing why 1 kbps is the appropriate design point for the target mission class (power, mass, antenna constraints for small satellites in the 50–500 unit range). Alternatively, present the 1 kbps analysis as a worst-case/stress-case and recommend 2–5 kbps as the nominal design point, which would simplify the entire framework.

**5. The GE channel model coherence assumption drives the key ARQ finding but is not independently justified.**

The per-cycle coherence assumption ($\tau_c \geq T_c$) makes intra-cycle ARQ "structurally ineffective by construction." The paper acknowledges this but still presents the 27% intra-cycle recovery as a finding. The physical justification (1 m panel at 2 m, 2°/s tumble → $\tau_c \approx 14$ s) applies to tumbling spacecraft, not to the stabilized spacecraft that would be performing coordinated operations.

*Why it matters:* The ARQ infeasibility finding and the consequent 35 kbps recommendation depend critically on this assumption. If $\tau_c < T_c$ (plausible for stabilized spacecraft with structural shadowing), intra-cycle ARQ becomes effective and 30 kbps may suffice.

*Remedy:* Present results for both $\tau_c \geq T_c$ (per-cycle coherence) and $\tau_c \ll T_c$ (independent per-attempt) as bounding cases. The paper already has the 98.9% delivery result for fast-fading; make this a co-equal design case rather than a footnote. The 35 kbps recommendation should be explicitly conditioned on the coherence regime.

---

## Minor Issues

1. **Eq. 7 framing term:** $T_{\text{framing}} = O_{\text{frame}} / (R_{\text{FEC}} \cdot R_{\text{PHY}})$ implies framing bits are FEC-encoded. This is stated as "CCSDS standard practice," but Proximity-1 actually places the ASM outside the FEC codeword. Verify whether the 104-bit overhead is entirely within the FEC block or partially outside it; the difference is ~1 ms at 30 kbps (small but non-negligible for margin calculations).

2. **Table I notation:** $p_{\text{exc}}$ is defined as "per-node per-cycle reporting probability" but the subscript "exc" suggests "exception." Clarify whether this is exception-only reporting or periodic reporting with probability < 1.

3. **Section III-B-2:** "Each cluster coordinator sends a single 512-byte summary per cycle" — the breakdown (48 + 48 + 13 + 32 + 371 = 512 B) allocates 371 B to "metadata/CRC," which seems excessive. A 32-bit CRC is 4 B; what occupies the remaining 367 B?

4. **Thundering herd footnote (Section III-B-2):** The BEB analysis assumes Slotted ALOHA, but the main protocol is TDMA. Clarify when the system transitions from TDMA to Slotted ALOHA (presumably only during coordinator failure/election).

5. **Table V (Feasibility Summary):** The "1-Cyc?" column shows checkmarks for broadcast full-load but "—" for unicast full-load. Add a footnote clarifying that "—" means "requires stagger" rather than "infeasible."

6. **Section IV-A:** "Phase-staggered scheduling... DES confirms zero drops at ≥25 kbps vs. 50 kbps under random phase." This is a significant finding buried in a single sentence. Elaborate or provide a figure.

7. **Eq. 4 (consensus overhead):** The formula uses $f_{\text{decision}}$ (decisions per cycle) but the stability limit ($f_{\text{decision,max}} \approx 24$) is stated without derivation. Show the derivation or cite it.

8. **Section IV-B (AoI):** The claim that AoI P99 = 441 s is "< 0.5% of a 24 h TCA window" is misleading—the relevant comparison is not the TCA window but the maneuver decision timeline, which can be much shorter for high-probability conjunctions.

9. **Abstract:** "γ₅₀ = 0.695 to γ₂₄ = 0.761; rate-dependent" — the subscript convention (PHY rate in kbps) should be stated explicitly in the abstract for clarity.

10. **Reference [55]:** The self-citation to the AI deliberation methodology report adds no technical value to this paper and should be removed or moved to the acknowledgment.

11. **Table III (Simulation Parameters):** The collision avoidance rate ($10^{-4}$/node/s) is described as a "conservative upper bound" but is 300× higher than the ESA-reported rate. "Stress-test parameter" would be more accurate than "conservative upper bound."

12. **Section V-C (Limitations):** "J2 analysis... cross-plane at ~0.014/orbit fleet-wide" — units are unclear. Is this re-associations per orbit per cluster? Per node?

13. **Algorithm 1, Line 3:** $\eta_0 = 5\%$ is hardcoded. For practitioners with different heartbeat sizes or coordinator summary sizes, this should be parameterized.

14. **Typographical:** "Eq.~\ref{eq:gamma_time}" is referenced before it appears in the document flow (introduced in Section I but defined in Section IV-J/V-C). Consider reordering or adding a forward reference note.

---

## Overall Recommendation
**Recommendation: Major Revision**

This paper makes a legitimate contribution by providing closed-form sizing equations and an actionable feasibility framework for hierarchical coordination in large space swarms. The two-layer decomposition (byte budget + TDMA airtime), the generalized $\gamma$ expression, the campaign duty factor parameterization, and Algorithm 1 are all useful tools for preliminary mission design. The paper's intellectual honesty—particularly the explicit validation gap acknowledgment, the claim map by evidence tier, and the careful labeling of the GE model as a design tool—is exemplary and sets a high standard for transparency.

However, the paper suffers from three fundamental weaknesses that must be addressed before publication. First, the validation architecture is almost entirely self-referential: the DES confirms the analytical equations, the slot simulator uses the same $\gamma$ formula, and the packet-level analysis is parameter estimation rather than validation. The paper needs at least one genuinely independent validation element (even a simplified NS-3 comparison) or must be substantially shortened to reflect its actual validation status. Second, the fleet-level claims ($10^5$ nodes) are not supported by the per-cluster analysis and should be either substantiated or removed from headline claims. Third, the manuscript is excessively long and repetitive, with numerous caveats and cross-references that, while individually correct, collectively obscure the core contribution. A 30–40% reduction in length, focusing on the essential framework and deferring secondary analyses to supplementary material, would substantially improve readability and impact.

The strongest elements—the generalized $\gamma$ expression, the rate ladder, the $\gamma$-conditional lookup table, and Algorithm 1—should be preserved and highlighted. With significant revision to address the validation gap, scope claims, and presentation density, this work could make a solid contribution to the preliminary design literature for large-scale space systems.

---

## Constructive Suggestions
*(Ordered by impact)*

1. **Add one independent validation element.** Even a 10-node NS-3 TDMA simulation comparing achieved throughput against the $\gamma$-predicted throughput would transform the validation status from "entirely self-referential" to "anchored in at least one independent tool." This is the single highest-impact improvement.

2. **Reduce manuscript length by 30–40%.** Merge Sections IV-A through IV-D into a single "TDMA Sizing and Loss Recovery" section. Move Model S entirely to an appendix. Eliminate redundant warnings and cross-references. The current length (~12,000 words of body text) exceeds typical IEEE T-AES limits.

3. **Restrict headline claims to per-cluster scope.** Change the title to include "per-cluster" or "single-cluster." Present fleet-level scaling as a clearly labeled extension with explicit caveats, not as a primary result.

4. **Present dual coherence-regime results.** Show the 30 kbps recommendation for $\tau_c \ll T_c$ alongside the 35 kbps recommendation for $\tau_c \geq T_c$. This doubles the practical utility of the ARQ analysis.

5. **Strengthen the 1 kbps justification.** Either derive it from a specific mission class's power/mass/antenna constraints or present 2–5 kbps as the nominal design point with 1 kbps as the stress case.

6. **Add a one-page "Quick Start" guide.** For practitioners: given your $k_c$, $S$, $T_c$, and measured $\gamma$, here is how to use Algorithm 1 in three steps. This would maximize the paper's practical impact.

7. **Provide a downloadable spreadsheet or web calculator** implementing Algorithm 1, in addition to the Python code. This lowers the barrier to adoption for mission designers who may not use Python.