---
paper: "02-swarm-coordination-scaling"
version: "cz"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-03-05"
recommendation: "Unknown"
---



# Peer Review: "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms" (Version CZ)

---

## 1. Significance & Novelty
**Rating: 3 (Adequate)**

The paper addresses a genuine gap: no prior work provides closed-form parametric sizing relationships for hierarchical coordination architectures at the $10^3$–$10^5$ node scale with byte-level traffic accounting. The two-test feasibility framework (byte budget + TDMA airtime) is a useful conceptual contribution, and the campaign duty factor $d$ is a sensible parameterization for episodic workloads. However, the novelty is tempered by the fact that the individual analytical components (M/D/1 queueing, GE channel models, TDMA slot accounting, AoI under geometric sampling) are well-established. The contribution is primarily one of *integration and parameterization* rather than fundamental methodological advance. The paper is honest about this, which is appreciated, but the practical impact remains uncertain without external validation. The claim of applicability to $10^5$–$10^6$ nodes is somewhat misleading given that all analysis is per-cluster ($k_c = 50$–$500$) and fleet-level scaling relies on an order-of-magnitude spatial reuse estimate.

## 2. Methodological Soundness
**Rating: 3 (Adequate)**

The analytical framework is internally consistent and the decomposition into Test A (byte budget) and Test B (TDMA airtime) is clean. The generalized $\gamma$ expression (Eq. 7) is well-derived from CCSDS Proximity-1 framing parameters. The campaign duty factor $d$ adequately addresses workload realism—the mapping in Table VI from mission phases to $d$ values, anchored by ESA conjunction statistics, is convincing. However, several methodological concerns remain:

- The DES verification is largely tautological (acknowledged by the authors as Tier 1 only), confirming its own equations to <0.1%. Its distributional contribution (buffer sizing under campaign burstiness) is modest and conditional on the assumed ON/OFF Markov campaign model.
- The slot-level simulator and packet-level simulator share the same equations as the analytical model, making cross-verification circular.
- The GE channel model is parameterized without any ISL measurement data; the per-cycle coherence assumption ($\tau_c \geq T_c$) is a strong structural choice that makes intra-cycle ARQ ineffective *by construction*.
- The centralized TDMA assumption (no contention) is a significant simplification that removes the most challenging aspect of MAC-layer design.

## 3. Validity & Logic
**Rating: 3 (Adequate)**

The gamma unification appears consistently applied: $\gamma_{24} = 0.761$, $\gamma_{30} = 0.745$, $\gamma_{35} = 0.732$ are derived from Eq. 7 and used throughout Tables IV, VII, VIII, and Algorithm 1. The earlier 0.85 value does not appear. The stress-case $\eta_S \approx 46\%$ is now properly contextualized as a continuous-duty upper bound occurring <1% of operational time (Section IV-E, Table VI), with the yearly mixture calculation ($\bar{\eta} = 5.6\%$) providing useful context.

The three-layer feasibility framework is logically sound, and the paper is careful to note that the heuristic (Eq. 14) is algebraically equivalent to Test B, not a separate check. However, I have concerns about logical completeness:

1. The assumption that coordinator ingress is the binding bottleneck implicitly assumes egress is always broadcast. For unicast-heavy workloads ($q \to 1$), egress becomes binding, and the 19-cycle stagger (190s) may interact with campaign duty cycles in ways not fully explored.

2. The fleet-level reuse analysis (Eq. 5) assumes $R = 3$ with only an order-of-magnitude justification ("$>$20 dB isolation at $\geq$500 km"). This is insufficient for a system claiming scalability to $10^5$ nodes.

3. The RF-backup analysis (thundering herd, Slotted ALOHA with BEB) is presented in a footnote but represents a critical failure mode. The claimed convergence in "2 doubling rounds (~640 ms)" followed by "140–160 s" election seems inconsistent—if BEB resolves contention in 640 ms, why does election take 160 s?

## 4. Clarity & Structure
**Rating: 4 (Good)**

The paper is well-organized with a clear roadmap. The notation table (Table I) is comprehensive. The explicit labeling of Model S vs. Model C throughout, with repeated warnings that Model S is "NOT for design," is effective. Algorithm 1 provides an actionable synthesis. The rate ladder (Table III) is a particularly clear presentation.

However, the paper is *extremely* dense. At approximately 12,000 words of technical content, it attempts to cover architecture, traffic modeling, TDMA scheduling, GE channel analysis, AoI, fleet scaling, buffer sizing, and validation—each of which could be a substantial section in its own right. This density leads to:
- Footnotes carrying critical technical content (e.g., the thundering herd analysis)
- Tables with extensive footnotes that are essential for interpretation
- Repeated defensive caveats ("not for design," "no external validation") that, while appropriate, consume space

The figures are well-chosen but the manuscript would benefit from consolidation.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**

The paper is exemplary in its transparency. The V&V tier structure (Section III-A) clearly delineates what is verified vs. validated. The claim map (Table IX) is an unusually honest assessment of evidence strength. The repeated acknowledgment that "no external validation exists" and "predictive accuracy for real ISL channels is unknown" sets an appropriate standard. Data availability is excellent (GitHub with tagged release). AI disclosure is specific and appropriate.

## 6. Scope & Referencing
**Rating: 3 (Adequate)**

The literature coverage is broad but has notable gaps:
- No reference to the extensive TDMA scheduling literature in cellular/satellite systems (e.g., Elson & Picholtz on TDMA synchronization, or the PRMA literature)
- The DVB-RCS2 comparison is acknowledged as imperfect (ground terminals, not ISL) but no closer analog is cited—what about CCSDS AOS or TC standards for actual space TDMA?
- Network calculus is cited but not used; a deterministic worst-case bound via network calculus would strengthen the analysis
- The mean-field game references (Lasry, Huang) seem tangential—they are cited but never connected to the analysis
- Missing references to recent small-sat ISL demonstrations (e.g., CLICK, LINCS) that could provide empirical $\gamma$ data

The paper is appropriate for IEEE T-AES in scope, though the lack of external validation is a significant concern for this venue.

---

## Major Issues

**1. Circular validation architecture**
- *Issue:* The DES, slot-level simulator, and packet-level simulator all implement the same equations. The <0.1% agreement between DES and analytical results is code verification, not model validation. The packet-level $\gamma$ derivation (Section IV-J) is a parameter computation from CCSDS standards, not independent validation.
- *Why it matters:* The paper's central claims (feasibility boundaries, PHY rate recommendations) rest entirely on unvalidated models. While the authors acknowledge this clearly, the extensive internal cross-checking may give readers a false sense of confidence.
- *Remedy:* (a) Reduce the emphasis on DES-analytical agreement; a single sentence suffices. (b) Pursue at least one form of external anchoring: NS-3 simulation of the TDMA MAC, or comparison with measured slot efficiencies from any operational TDMA satellite system (even if not ISL). (c) If no external validation is feasible pre-publication, restructure the paper explicitly as a "design methodology" contribution rather than a "results" contribution.

**2. Fleet-level scaling claims are unsupported**
- *Issue:* The abstract and introduction claim applicability to $10^3$–$10^5$ nodes, but all analysis is per-cluster. Fleet scaling relies on Eq. 5 ($T_c^{\text{fleet}} = G \cdot T_c$) with $R = 3$ justified only by ">20 dB isolation at ≥500 km"—an assertion without link budget detail, antenna pattern analysis, or interference modeling.
- *Why it matters:* Inter-cluster interference is the primary scaling challenge for fleet-level TDMA. Claiming $10^5$-node scalability without addressing this is a significant gap.
- *Remedy:* Either (a) provide a proper interference analysis with realistic antenna patterns and geometry, or (b) explicitly restrict all claims to per-cluster sizing and remove fleet-level scaling from the abstract and conclusions.

**3. The GE model's structural assumptions predetermine key results**
- *Issue:* The per-cycle coherence assumption ($\tau_c \geq T_c$) makes intra-cycle ARQ structurally ineffective by construction (27% recovery). The authors acknowledge this ("not an emergent finding") but then present the dual coherence-regime recommendation as a key result.
- *Why it matters:* The recommendation to use 35 kbps (for slow-mixing) vs. 30 kbps (for fast-fading) is entirely driven by this assumption, not by analysis. Without ISL channel measurements, the coherence regime is unknown, making the recommendation unactionable.
- *Remedy:* (a) Present the GE analysis purely as a sensitivity tool (which it is), not as a basis for PHY rate recommendations. (b) Provide the $R_{\text{PHY,min}}$ as a function of $\tau_c / T_c$ explicitly, so practitioners can select based on measured coherence. (c) Remove the "dual coherence-regime recommendation" framing from the conclusion.

**4. Coordinator failure analysis is incomplete**
- *Issue:* The RF-backup failure mode suspends hierarchical coordination entirely (Table II), yet the paper claims 99.5% availability. The thundering herd analysis (footnote 1) estimates 140–160 s recovery, but this is for Raft election only—it does not account for TDMA schedule re-establishment, state synchronization, or the possibility that the new coordinator lacks current cluster state.
- *Why it matters:* For a system claiming autonomous operation, the failure/recovery transient is a critical design driver. A 160+ second coordination gap in a 100-node cluster is operationally significant.
- *Remedy:* (a) Promote the failure analysis from a footnote to a proper subsection. (b) Include state recovery time (how does the new coordinator obtain current cluster state if optical ISL is unavailable?). (c) Quantify the availability claim with a proper Markov availability model including all failure modes and recovery times.

**5. The 1 kbps per-node budget needs stronger justification**
- *Issue:* The paper acknowledges this is a "baseline design target" not a hard limit, and provides a physical justification (200 kbps aggregate / 100 nodes × 0.75 ≈ 1.5 kbps). However, the 200 kbps aggregate capacity is itself unvalidated—it comes from a link budget (Section IV-A) that is stated but not fully derived.
- *Why it matters:* The entire feasibility analysis is conditioned on this budget. If the actual per-node capacity is 2 kbps, stress-case overhead halves to ~23% and the paper's main tension (tight margins at 1 kbps) disappears. If it's 0.5 kbps, the architecture is infeasible.
- *Remedy:* Provide the complete S-band ISL link budget as a table (transmit power, antenna gain, path loss, noise figure, coding gain, margin) so readers can verify the 200 kbps aggregate and assess sensitivity to link budget assumptions.

---

## Minor Issues

1. **Table I notation:** $\alpha_{\text{RX}}$ is listed as "derived from schedule" but its default value (0.908) appears in multiple places before Algorithm 1 derives it. Clarify that 0.908 is the value at 30 kbps, $M_r = 0$.

2. **Eq. 1 inconsistency:** $M_{\text{total}}$ counts messages but is never used in subsequent analysis. Either connect it to $\eta$ or remove it.

3. **Section III-B.2, coordinator summary:** "mean orbital elements (48 B), covariance (6 elements × 8 B = 48 B), health/alert bitfield (100 bits = 13 B), anomaly flags (32 B), and metadata/CRC (371 B)" sums to 512 B, but 371 B of "metadata/CRC" is suspiciously large. Justify or decompose.

4. **Table V (superframe):** The sync beacon is listed as "8 bits at 30 kbps = 0.3 ms." A sync beacon of 8 bits seems implausibly short—even a minimal ASM is 32 bits. Clarify whether this is a placeholder.

5. **Eq. 6 (consensus):** The formula assumes serialized votes over a shared channel but doesn't account for the TDMA slot structure. How are Raft messages scheduled within the TDMA frame?

6. **Section IV-B (AoI):** The statement "AoI P99 = 441 s is <0.5% of a 24 h TCA window" conflates two different timescales. AoI is about state freshness for coordination; TCA windows are about conjunction assessment. These serve different operational needs.

7. **Fig. 2 description:** "DES bars (30 MC replications, N = 10,000, k_c = 100)" — the figure shows a CDF but is described as having "bars." Clarify whether this is a histogram or empirical CDF.

8. **Table VII (rate feasibility):** The margin column should specify whether it includes egress (192 ms) or not. The footnote says "Margin = T_c − Ingress − 192 ms" but this should be in the column header.

9. **Typo/style:** "Eq.~\ref{eq:gamma_derived}" is referenced as "Model S" in some places and "simplified" in others. Standardize terminology.

10. **Reference [43] (Alfano):** Cited in the bibliography but never referenced in the text. Remove or add a citation.

11. **Abstract length:** At ~250 words, the abstract is dense but within IEEE limits. However, the phrase "CCSDS Proximity-1 framing anchors γ ≈ 0.70–0.76 (rate-dependent)" is too detailed for an abstract.

12. **Algorithm 1, Line 4:** The footnote states this is "algebraically equivalent to Eq. 7" but the expression in Line 4 groups terms differently. Show the equivalence explicitly or remove the claim.

---

## Overall Recommendation
**Recommendation: Major Revision**

This manuscript makes a legitimate contribution by providing a structured, closed-form sizing framework for hierarchical coordination in large space swarms. The two-test feasibility decomposition (byte budget + TDMA airtime), the campaign duty factor parameterization, and the generalized $\gamma$ expression are useful tools for preliminary system design. The paper's transparency about its limitations—particularly the absence of external validation—is commendable and sets a good standard.

However, the paper suffers from three fundamental weaknesses that require major revision. First, the validation architecture is entirely circular: all internal tools share the same equations, and the extensive cross-checking provides code verification but no model validation. The packet-level $\gamma$ derivation is a parameter computation, not independent validation. The paper needs either genuine external anchoring (NS-3, hardware measurements, or comparison with operational systems) or a significant restructuring to present itself as a design methodology rather than validated results. Second, fleet-level scaling claims ($10^5$ nodes) are unsupported beyond per-cluster analysis; the spatial reuse estimate ($R = 3$) lacks the interference analysis needed to justify these claims. Third, the GE channel model's structural assumptions predetermine the key PHY rate recommendations, making them unactionable without ISL channel measurements that do not yet exist.

The paper's strengths—rigorous internal consistency, honest self-assessment, actionable Algorithm 1, and comprehensive parameter sensitivity—provide a strong foundation for revision. The most impactful improvements would be: (1) obtaining at least one form of external validation (even partial), (2) restricting claims to per-cluster sizing, and (3) reframing the GE analysis and PHY recommendations as sensitivity tools rather than design prescriptions.

---

## Constructive Suggestions
*(Ordered by impact)*

1. **Obtain external anchoring for $\gamma$.** Even a single data point from an operational TDMA satellite system (e.g., published DVB-RCS2 terminal measurements, or CCSDS Proximity-1 modem bench tests) would transform the validation status. Contact CCSDS working groups or ESA/NASA ISL development programs for measured slot efficiency data.

2. **Restrict fleet-level claims.** Reframe the paper as "per-cluster sizing equations" and present fleet scaling as a future direction requiring interference analysis. This is more honest and actually strengthens the paper by focusing on what is well-supported.

3. **Provide the complete S-band link budget as a table.** This is straightforward and allows readers to verify the 1 kbps budget and assess sensitivity.

4. **Consolidate the DES contribution.** The DES adds value only through distributional tail analysis (Fig. 3). Reduce DES-analytical agreement discussion to one paragraph and expand the buffer sizing analysis with additional campaign models (e.g., heavy-tailed).

5. **Present $R_{\text{PHY,min}}$ as a continuous function of $\tau_c/T_c$.** This replaces the binary "dual coherence-regime" recommendation with a practitioner-usable design curve.

6. **Expand the coordinator failure analysis** into a proper subsection with a Markov availability model covering optical-normal, S-band coordination, and RF-backup states.

7. **Add a "design example" subsection** walking through Algorithm 1 for a specific mission (e.g., a 10,000-node LEO constellation with known orbital parameters), demonstrating practical utility.

8. **Consider network calculus bounds** as a complement to the mean-value analysis. Since Le Boudec is already cited, a deterministic worst-case bound on coordinator ingress delay would strengthen the TDMA feasibility analysis.