---
paper: "02-swarm-coordination-scaling"
version: "cb"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-28"
recommendation: "Unknown"
---



# Peer Review: Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms (Version CB)

---

## 1. Significance & Novelty
**Rating: 3 (Adequate)**

The paper addresses a genuine gap: no prior work provides closed-form parametric sizing relationships for hierarchical coordination at the $10^3$–$10^5$ node scale with byte-level traffic accounting. This is a useful contribution for systems engineers sizing future mega-constellations and swarm architectures. However, the novelty is tempered by several factors: (a) the core analytical results are relatively straightforward accounting equations (linear byte budgets, geometric AoI, standard GE Markov chains) rather than fundamentally new theory; (b) the most interesting finding—that command traffic dominates and is topology-invariant under centralized generation—is somewhat intuitive once stated; (c) the 1 kbps RF-backup regime, where the framework is most needed, is acknowledged to apply <1% of operational lifetime. The three-layer feasibility decomposition (byte budget, MAC efficiency, TDMA airtime) is a clean conceptual contribution, though each layer individually uses well-established methods.

## 2. Methodological Soundness
**Rating: 3 (Adequate)**

The methodology is internally consistent but raises several concerns:

**Campaign duty factor (d).** The introduction of $d$ is a significant improvement that properly contextualizes the stress-case. The linear model $\eta(d) = \eta_0 + d \cdot \eta_{\text{cmd}}$ is clean and useful. However, the Bernoulli per-cycle model for campaign activity is simplistic—real campaigns exhibit temporal correlation (orbit-raising campaigns last days, not random cycles). The bimodal distribution in Fig. 7 partially captures this but the model doesn't account for campaign duration statistics.

**DES verification value.** The authors are commendably transparent that DES-analytical agreement is "expected by construction." The claimed independent DES contribution—distributional analysis of coordinator ingress variability (Fig. 7)—is modest. The bimodal CDF under stochastic $d$ is predictable from the mixture model. The DES does serve as a useful implementation cross-check, but its verification value beyond confirming its own equations is limited.

**Packet-level validation (Section IV-J).** The CCSDS-grounded $\gamma$ derivation is the strongest validation element. It provides genuine independent grounding by deriving $\gamma = 0.76$ from physical-layer standards rather than assuming it. However, calling this "packet-level validation" slightly overstates the case—it is a standards-grounded parameter derivation, not a full packet-level simulation with contention, retransmission protocols, and realistic traffic patterns.

**Three-layer feasibility framework.** The decomposition is sound in principle. Layer 1 (byte budget) and Layer 2 (MAC efficiency) are cleanly separated. Layer 3 (TDMA airtime) correctly identifies the half-duplex scheduling constraint that the other layers miss. The framework's value is demonstrated by the unicast stagger result (Eq. 12), which shows a workload that passes Layers 1–2 but fails Layer 3.

## 3. Validity & Logic
**Rating: 3 (Adequate)**

**Gamma unification.** The replacement of the earlier $\gamma = 0.85$ with the CCSDS-derived $\gamma = 0.76$ is consistently applied throughout the paper. The decomposition (Eq. 7, Table IX) is transparent and traceable. This is a clear improvement over earlier versions.

**Stress-case contextualization.** The $\eta_S \approx 46\%$ is now properly framed as a continuous-duty upper bound ($d = 1$), with Table VII showing the realistic operating range ($d = 0.01$–$0.10$, $\eta \approx 5$–$10\%$). This addresses the earlier concern about workload realism effectively.

**Logical concerns remain:**

1. The coordinator failure analysis (Section III-B) claims compound probability of $6.3 \times 10^{-12}$ s$^{-1}$ for simultaneous ISL outage and coordinator failure. This assumes independence between ISL outage and coordinator failure, which may not hold (e.g., a solar particle event could cause both).

2. The GE model's coherence assumption ($T_c$-scale transitions) is stated as "conservative for recovery" but this depends on the obstruction mechanism. The paper acknowledges this (three-mechanism taxonomy) but the default parameterization conflates structurally different phenomena.

3. The claim that overhead is "scale-invariant" ($\eta = O(1)$) is true by construction of the hierarchical model but obscures that the *absolute* byte budget per node is fixed at 1 kbps—the overhead fraction is constant because both numerator and denominator scale with $N$.

## 4. Clarity & Structure
**Rating: 4 (Good)**

The paper is well-organized with a clear roadmap (Section IV preamble), consistent notation (Table I), and systematic cross-referencing. The three-layer framework provides a useful organizing principle. Specific strengths:

- Table III (bandwidth scaling across regimes) immediately communicates when the framework is binding
- Table VIII (schedulability) cleanly maps workloads to feasibility layers
- The claim map (Table XII) is exemplary for transparency

Weaknesses:
- The paper is very long (~15 pages of dense technical content) with substantial redundancy between the introduction, results, discussion, and conclusion
- Some figures are referenced but their content is described rather than shown (the review assumes they exist as described)
- The operational context paragraph in Section I could be elevated to reduce confusion about when the 1 kbps regime applies

## 5. Ethical Compliance
**Rating: 5 (Excellent)**

Exemplary data availability: open-source code, tagged release, full parameter tables, MC configuration, and multiple simulation tools. The AI disclosure is explicit and appropriately scoped. Reproducibility is well-supported.

## 6. Scope & Referencing
**Rating: 3 (Adequate)**

The reference list covers the major relevant areas (CCSDS standards, swarm robotics, constellation management, distributed systems, AoI theory). Notable gaps:

- No references to actual TDMA implementations in space (e.g., TDRS, or ESA's proximity link protocols in practice)
- Limited engagement with the network calculus literature beyond a single citation—Le Boudec's framework could provide complementary worst-case bounds
- No references to recent work on LEO constellation autonomous operations (e.g., Telesat Lightspeed's autonomous collision avoidance)
- The Lutz et al. [1991] reference for GE parameterization is appropriate but dated; more recent ISL channel measurements (e.g., from optical ISL campaigns on Starlink or EDRS) would strengthen the physical grounding

---

## Major Issues

**1. The DES provides limited independent validation beyond implementation consistency.**

The paper is transparent about this (Section IV-F), but the verification taxonomy (IEEE 1012) creates an impression of multi-level assurance that is stronger than warranted. The DES, slot-level simulator, and analytical equations all implement the same message-layer model with the same assumptions. The distributional contribution (Fig. 7) is real but modest—a mixture of two known distributions under Bernoulli campaign switching.

*Why it matters:* Readers may overestimate the validation depth. The paper's actual validation rests almost entirely on the CCSDS $\gamma$ derivation and the slot-level TDMA timing check.

*Remedy:* Restructure the verification narrative to clearly distinguish (a) implementation cross-checks (DES vs. analytical—expected agreement), (b) model-level verification (slot-level TDMA—confirms superframe feasibility under half-duplex constraints not captured by the fluid model), and (c) standards grounding ($\gamma$ derivation—the only element that brings external data). Reduce the emphasis on DES-analytical agreement.

**2. The generalized $\gamma$ expression (Eq. 17) conflates independent physical mechanisms.**

The multiplicative decomposition $\gamma = \gamma_{\text{framing}} \times \gamma_{\text{FEC}} \times \gamma_{\text{guard}} \times \gamma_{\text{acq}}$ assumes these factors are independent, but FEC overhead and framing overhead interact (FEC encodes the framed packet, not just the payload), and acquisition time may depend on guard interval allocation. More importantly, the expression omits several real-world factors: synchronization overhead, ranging, protocol handshaking, and thermal/clock drift compensation.

*Why it matters:* Practitioners using Eq. 17 may underestimate the gap between computed and realized $\gamma$.

*Remedy:* (a) Clarify that the multiplicative model is an approximation; (b) add a "residual inefficiency" term $\gamma_{\text{margin}}$ (suggest 0.90–0.95) to account for unmodeled factors; (c) validate against at least one real TDMA space link's measured efficiency if data are available.

**3. The topology comparison is structurally asymmetric and potentially misleading.**

The centralized baseline models only compute-queue scalability (not communication overhead), the global-state mesh is an intentional worst case, and the sectorized mesh has different functional scope. This means the hierarchical architecture is never compared against a peer architecture with equivalent functional capability. The paper acknowledges this (Table VI), but the visual comparison (Fig. 8) may still mislead casual readers.

*Why it matters:* The paper's framing suggests the hierarchical approach is superior, but it is compared only against intentional bounds and a functionally different system.

*Remedy:* Either (a) add a federated/peer-to-peer architecture with equivalent functional scope as a true comparator, or (b) more prominently frame the comparison as "bounding analysis" rather than "architecture comparison" throughout (including figure captions and table titles).

**4. The static topology assumption needs stronger justification for cross-plane configurations.**

The J2 perturbation analysis (Section V-B) shows re-association is infrequent for Walker constellations, but this analysis assumes a specific constellation geometry. For non-Walker configurations (e.g., heterogeneous orbits, elliptical orbits, or debris-avoidance maneuvers), cluster membership may change much more frequently. The <0.3% overhead estimate is constellation-specific, not general.

*Why it matters:* The paper claims generality across $10^3$–$10^5$ nodes, but the static topology assumption limits applicability to specific orbital configurations.

*Remedy:* (a) State the static-topology assumption as a limitation that restricts applicability to near-circular, co-altitude constellations; (b) provide a parameterized re-association overhead formula that practitioners can evaluate for their specific constellation; (c) discuss the AoI transient during re-association more quantitatively.

**5. The 1 kbps design point lacks sufficient operational justification.**

The link budget (Table IV) shows the UHF omnidirectional backup achieves ~2.5 kbps maximum, justifying 1 kbps as conservative. However, the paper does not adequately justify why an omnidirectional UHF backup is the right operational concept. Modern small satellites increasingly use S-band or X-band patch antennas with modest gain (3–6 dBi) that could provide 10–100 kbps even in "backup" mode. The entire TDMA feasibility analysis (the paper's most technically interesting contribution) is relevant only at 1 kbps.

*Why it matters:* If the 1 kbps constraint is not well-motivated, the paper's most constrained (and interesting) analysis applies to a scenario that may not arise in practice.

*Remedy:* (a) Provide a more thorough operational concept for the RF backup, including why omnidirectional is required (e.g., tumbling spacecraft, unknown attitude); (b) acknowledge that a 10 kbps backup would eliminate all TDMA constraints; (c) frame the 1 kbps analysis as a worst-case sizing exercise rather than a baseline design.

---

## Minor Issues

1. **Table I notation:** $\gamma$ is defined as $T_{\text{data}}/T_{\text{slot}}$ but the CCSDS derivation shows it includes FEC and acquisition—these are not "slot" effects. Consider redefining as "effective MAC efficiency" or "channel utilization factor."

2. **Eq. 2:** $M_{\text{total}}$ counts messages but the overhead metric $\eta$ counts bytes. The connection between these should be made explicit.

3. **Section III-A:** "Atomic unit is a message-layer event" but the slot-level simulator operates at slot granularity. Clarify the relationship between these two simulation tools earlier.

4. **Table V (link budget):** Implementation loss of 2 dB is optimistic for a UHF omnidirectional system; 3–4 dB is more typical when including polarization mismatch, cable losses, and impedance mismatch.

5. **Section IV-A:** "Fleet-wide TDMA cost is 0.28 kbps/node (1% coordinators at $k_c = 100$)"—this assumes uniform cluster sizes. Uneven clusters would change the fleet-average cost.

6. **Eq. 11 (AoI):** The ceiling function introduces a discretization artifact of up to $T_c$. The text notes "consistent within one $T_c$ step" but should state this is inherent to the discrete-cycle model, not a simulation artifact.

7. **Section IV-C:** "Coherence assumption: the GE state transitions once per $T_c$"—this is a modeling choice, not a physical property. The text should more clearly separate the model assumption from the physical justification.

8. **Table VII:** The "TDMA?" column threshold ($\eta_{\text{total}}/\gamma > 50\%$) should be derived or referenced, not just stated.

9. **Fig. 3 caption:** "Phase staggering eliminates drops at ~25 kbps vs. 50 kbps under random phase"—the 2× improvement factor should be explained physically (burst spreading).

10. **Section V-B:** "MTTF = 50 yr, consistent with LEO small-satellite data [Castet]"—Castet's data are from pre-2009 satellites; modern small-sat reliability may differ significantly.

11. **Typo/style:** "conjunction challenges" (Introduction)—"challenges" is vague; specify (e.g., "conjunction screening workload" or "collision avoidance maneuver frequency").

12. **Reference [1]:** The Starlink FCC filing is cited for operational coordination, but FCC filings describe spectrum/orbit parameters, not coordination architecture. A more appropriate reference would be conference papers or press releases describing Starlink's autonomous collision avoidance.

13. **Eq. 17 ($\gamma$ general):** Units are inconsistent—$T_{\text{guard}}$ and $T_{\text{acq}}$ in ms but $R_{\text{PHY}}$ in bps; the "/1000" conversion factor is error-prone. Use consistent units.

14. **Section IV-J:** "Earlier versions: 0.850, Now superseded" in Table IX—this internal revision history is inappropriate for a journal publication. Remove or rephrase.

---

## Overall Recommendation
**Recommendation: Major Revision**

This paper makes a useful contribution by providing closed-form sizing equations for hierarchical coordination in large autonomous space swarms, filling a genuine gap between swarm robotics (tens of agents) and constellation management (ground-controlled). The three-layer feasibility framework is a clean conceptual contribution, and the CCSDS-grounded $\gamma$ derivation provides meaningful physical-layer anchoring. The campaign duty factor $d$ effectively addresses earlier concerns about workload realism, and the stress-case is now properly contextualized as a continuous-duty upper bound.

However, several issues require substantive revision. The verification narrative overstates the independence of the DES from the analytical model—the genuine validation rests on the slot-level TDMA timing and the $\gamma$ derivation, not on DES-analytical agreement. The topology comparison is structurally asymmetric, comparing the hierarchical architecture only against intentional bounds rather than functional peers. The 1 kbps design point, which drives the paper's most interesting analysis, needs stronger operational justification. The generalized $\gamma$ expression, while useful in concept, needs qualification regarding its multiplicative independence assumption and unmodeled factors.

The paper would benefit from tightening: reducing redundancy between sections, sharpening the distinction between implementation verification and model validation, and being more explicit about the narrow operational regime (RF backup during ISL outage) where the full framework is needed. With these revisions, the paper would make a solid contribution to the systems engineering literature for large-scale space architectures.

---

## Constructive Suggestions
*(Ordered by impact)*

1. **Restructure the verification narrative** around three clearly distinguished levels: implementation cross-check, model verification, and standards grounding. De-emphasize DES-analytical agreement; elevate the slot-level TDMA and $\gamma$ derivation as the primary verification contributions.

2. **Add a residual inefficiency factor** to the generalized $\gamma$ expression and validate against measured TDMA efficiency from at least one operational space link (TDRS, Proximity-1 heritage, or published ISL measurements).

3. **Strengthen the 1 kbps operational justification** with a clear concept of operations for the RF backup mode (when it activates, why omnidirectional is required, expected duration, and what coordination functions must survive).

4. **Reframe the topology comparison** as a bounding analysis throughout, or add a functionally equivalent peer architecture (e.g., flat Raft-based coordination without hierarchy).

5. **Extend the campaign duty factor model** to include temporal correlation (e.g., campaigns of geometric duration rather than i.i.d. Bernoulli per cycle), which would make the distributional analysis (Fig. 7) more realistic and the DES contribution more meaningful.

6. **Add a practitioner-oriented design flowchart** that guides users through the three feasibility layers with decision points, making the framework immediately actionable.

7. **Tighten the paper** by ~20%: consolidate the introduction's contribution list with the conclusion; merge Tables IV and VI into the link budget discussion; reduce repetition of the "$\gamma = 0.76$ validated" phrase (appears >10 times).

8. **Update the reliability reference** (Castet 2009) with more recent small-satellite reliability data, or acknowledge the temporal gap explicitly.