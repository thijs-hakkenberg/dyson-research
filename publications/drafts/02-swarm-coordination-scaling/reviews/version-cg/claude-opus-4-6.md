---
paper: "02-swarm-coordination-scaling"
version: "cg"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-03-01"
recommendation: "Unknown"
---



# Peer Review: Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms

## 1. Significance & Novelty
**Rating: 3 (Adequate)**

The paper addresses a genuine gap: no prior work provides closed-form parametric sizing relationships for hierarchical coordination at the $10^3$–$10^5$ node scale with byte-level traffic accounting. The two-layer feasibility framework (byte budget + TDMA airtime) and the decomposition into $\eta_0$ and $\eta_{\text{cmd}}$ are useful conceptual contributions. However, the novelty is tempered by the fact that the individual analytical components (M/D/1 queueing, GE channel models, AoI geometric analysis, TDMA slot budgets) are well-established; the contribution is primarily in their systematic assembly for this application domain. The practical impact depends heavily on whether the assumed message model and centralized command generation are representative of future autonomous swarm architectures—a point the authors acknowledge but do not resolve.

## 2. Methodological Soundness
**Rating: 3 (Adequate)**

The analytical framework is internally consistent and the three-layer verification hierarchy (analytical → DES → slot-sim/packet-sim) is well-structured. The campaign duty factor $d$ is a welcome addition that substantially improves workload realism compared to presenting only the stress-case. The CCSDS-grounded $\gamma$ derivation (replacing the earlier 0.85) is a meaningful methodological improvement.

However, several methodological concerns remain: (1) The DES is cycle-aggregated and message-layer only—it cannot capture the phenomena most likely to invalidate the sizing equations (MAC contention, antenna scheduling, multi-cluster interference). (2) The GE channel model is acknowledged as illustrative, with no ISL-specific measurement data. (3) The static cluster membership assumption, while justified for bandwidth sizing, limits applicability to dynamic LEO environments. (4) The fluid-server coordinator model in the DES cannot capture the TDMA-specific interactions that the slot-level simulator reveals, raising questions about which tool's results should be trusted for design decisions.

## 3. Validity & Logic
**Rating: 4 (Good)**

The internal logic is generally sound. The $\gamma$ unification is consistently applied: $\gamma_{24} = 0.760$ and $\gamma_{30} = 0.745$ from CCSDS Proximity-1 framing are used for all feasibility claims, with Model S ($\gamma = 0.949$) clearly labeled as an upper bound. The stress-case ($\eta_S \approx 46\%$) is now properly contextualized as a continuous-duty upper bound applying $<$1% of operational time, with representative campaign scenarios anchoring $d$ in concrete mission phases. The three-layer feasibility framework is logically coherent: byte budget → MAC translation → TDMA airtime, with clear binding conditions for each layer.

One logical tension: the paper claims the 1 kbps RF-backup channel is the "only regime requiring the TDMA schedulability analysis" (Section I), yet the coordinator operates at 24–30 kbps PHY. The TDMA analysis is really about coordinator ingress scheduling at the cluster level, not about the per-node 1 kbps budget. This conflation recurs and should be clarified.

## 4. Clarity & Structure
**Rating: 3 (Adequate)**

The paper is ambitious in scope and generally well-organized, with the roadmap at the beginning of Section IV being helpful. The notation table, canonical overhead definitions, and Algorithm 1 are valuable for practitioners. However, the manuscript suffers from excessive length and density. At approximately 12,000+ words of technical content (excluding references), it substantially exceeds typical IEEE T-AES page limits. The repeated disambiguation of Model S vs. Model C, while necessary, becomes tedious. Several tables could be consolidated. The paper would benefit from moving some sensitivity analyses (e.g., FEC rate sensitivity, coherence-time sensitivity) to supplementary material.

The figures are referenced appropriately but I cannot evaluate their quality directly. The claim map (Table IX) is an excellent addition for transparency.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**

Exemplary. Open-source code with tagged release, full parameter tables, Monte Carlo configuration details, runtime estimates, and explicit AI disclosure. The verification tier framework (adapted from IEEE 1012) with honest acknowledgment of what is and isn't validated is a model for the field. The "non-archival" labels on web sources are appropriate.

## 6. Scope & Referencing
**Rating: 3 (Adequate)**

The reference list covers the major relevant areas (CCSDS standards, swarm robotics, constellation management, distributed systems, AoI theory). However, several gaps exist: (1) No references to actual TDMA scheduling in space systems (e.g., CCSDS CFDP, actual ISL MAC protocols used in Iridium NEXT or Starlink). (2) The network calculus reference (Le Boudec) is mentioned once but not meaningfully engaged with—given that network calculus provides exactly the kind of worst-case deterministic bounds this paper claims to complement, a deeper comparison is warranted. (3) No references to recent work on distributed TDMA in ad-hoc networks or cognitive radio, which is directly relevant to the multi-cluster channel reuse problem. (4) The Lutz et al. reference is for land-mobile satellite channels; the paper should cite ISL propagation studies if any exist, or more explicitly state the absence.

---

## Major Issues

**1. The DES provides limited independent validation beyond confirming its own equations.**

The paper acknowledges (Section V-A, Tier 1) that DES-analytical agreement is "expected by construction." The DES's claimed additional value—distributional analysis (Fig. 7)—is useful but modest: it shows bimodal ingress under stochastic campaigns, which is qualitatively predictable from the ON/OFF model structure. The DES cannot capture MAC contention, antenna scheduling, or multi-cluster interference—precisely the phenomena that could invalidate the sizing equations. The paper should either (a) more explicitly bound the DES's contribution to distributional characterization and parameter sensitivity, downgrading claims about "verification," or (b) implement at least a simplified contention model within the DES to provide genuine cross-model validation.

*Why it matters:* Reviewers and practitioners need to understand what confidence level the DES actually provides. Calling it "verification" overstates the evidence.

*Remedy:* Revise Section III-A and V-A to consistently use "internal consistency check" rather than "verification" for DES-analytical agreement. Quantify the distributional insights (e.g., what buffer sizing margin does the bimodal finding imply beyond the closed-form mean?) to justify the DES's computational cost.

**2. The packet-level validation (Section IV-J) derives $\gamma$ but does not independently validate the sizing equations.**

Section IV-J constructs a packet-level simulator that derives $\gamma = 0.76$ from CCSDS framing—a valuable anchoring exercise. However, this is a parameter derivation, not a validation of the feasibility framework. The $\gamma$ value is then fed back into the same analytical equations. No packet-level end-to-end simulation confirms that the superframe actually works under realistic conditions (packet-level contention, acquisition failures, timing jitter beyond the assumed 1 ms). The cross-model consistency claimed in Section IV-J-2 ("all four models agree on ingress ≈ 9,445 ms") is circular: all four models use the same slot duration formula with the same $\gamma$.

*Why it matters:* The paper's central claim—that 30 kbps is the minimum viable PHY rate—rests entirely on the analytical slot budget. Without independent packet-level confirmation under realistic conditions, this remains an analytical prediction, not a validated design point.

*Remedy:* Either (a) implement a packet-level simulation that models acquisition failures, timing jitter, and FEC decoding delays as stochastic processes (not just efficiency factors), or (b) explicitly acknowledge that the 30 kbps design point is an analytical prediction requiring packet-level validation, and remove the term "validation" from Section IV-J's title.

**3. The 363 ms margin at 30 kbps (Model C) is uncomfortably thin and insufficiently stress-tested.**

Table V shows 363 ms unallocated margin in the TDMA superframe at 30 kbps. This is 3.6% of $T_c$. The paper identifies several unmodeled overheads (ranging ~50 ms, control-plane traffic, clock drift) but does not systematically account for them. Under GE steady-state, the expected retransmission airtime (~755 ms) already exceeds this margin, as the paper acknowledges. The compound effect of timing jitter, acquisition variability, and Doppler-induced slot drift could easily consume the remaining margin.

*Why it matters:* A 3.6% margin is below typical engineering practice for space systems (10–20% margin is standard at PDR level). If the margin is negative under realistic conditions, the minimum viable PHY rate shifts to ~35–40 kbps, changing the paper's central design recommendation.

*Remedy:* Add a margin analysis that accounts for all identified unmodeled overheads (ranging, control-plane, clock drift, acquisition variability) with conservative estimates. If the margin becomes negative, revise the minimum viable PHY rate recommendation accordingly. Consider presenting a margin vs. PHY rate curve.

**4. The centralized command generation assumption limits the framework's generality.**

The paper repeatedly notes that $\eta_{\text{cmd}}$ is "topology-invariant given the assumed workload semantics (centralized command generation)." This is a strong assumption that may not hold for autonomous swarms—the very systems the paper targets. Section IV-A briefly mentions that cluster-local Raft consensus yields $\eta_{\text{consensus}} = 3.1\%$ per decision (and later 30.7% in Section IV-E), but these numbers are inconsistent and not integrated into the feasibility framework. For a paper claiming to provide "design equations for autonomous space swarms," the inability to size distributed decision architectures is a significant limitation.

*Why it matters:* Autonomous swarms are likely to use distributed planning, not centralized command generation. The framework's utility for its stated target application is reduced.

*Remedy:* Reconcile the 3.1% and 30.7% Raft consensus overhead figures (they appear to measure different things—clarify). Provide a worked example showing how the sizing equations adapt for cluster-local planning, even if approximate. This would substantially increase the paper's practical value.

**5. The GE channel model lacks empirical grounding for ISL applications.**

The paper honestly acknowledges that "no ISL-specific GE measurement data are available in the open literature" and that the default parameterization "should be treated as illustrative rather than predictive." While the sensitivity sweep (Fig. 5b) partially addresses this by providing design curves across the parameter space, the paper's specific numerical claims (P95 = 4 cycles, mean = 1.7 cycles) are conditioned on illustrative parameters. The mechanism-to-parameter mapping (Table IV) provides estimated ranges but no empirical basis.

*Why it matters:* The GE recovery analysis is one of the paper's three main contributions. Without empirical grounding, its practical utility is limited to providing a methodology rather than actionable design numbers.

*Remedy:* (a) More prominently caveat all GE-derived numerical results as illustrative. (b) Identify specific measurement campaigns that could provide ISL-specific GE parameters (e.g., from Iridium NEXT or Starlink ISL operational data). (c) Consider whether a simpler model (e.g., availability-based with conservative blockage duration) might be more defensible for design purposes.

---

## Minor Issues

1. **Inconsistent Raft consensus overhead:** Section IV-A states $\eta_{\text{consensus}} = 3.1\%$ per decision (3,840 B); Section IV-E states $\eta_{\text{consensus}} \approx 30.7\%$. The former appears to be per-decision, the latter per-cycle under continuous consensus. Clarify the distinction explicitly where both appear.

2. **Equation (5) units:** The general $\gamma$ expression (Eq. 5) mixes bits, ms, and bps with a $10^{-3}$ conversion factor. While dimensionally correct, this is error-prone for practitioners. Consider presenting the time-domain form (Eq. 6) as primary, with the bit-domain form as an alternative.

3. **Table I notation:** $\alpha_{\text{RX}}$ is defined as "ingress fraction of $T_c$ (0.944 at $k_c = 100$, 30 kbps Model C)" but Table V shows ingress = 9,445 ms = 0.9445 of $T_c$. The 0.944 value appears to exclude egress allocation. Clarify whether $\alpha_{\text{RX}}$ is the ingress time fraction or the RX-allocated fraction.

4. **Section III-B-2, coordinator failure transient:** The compound probability $6.3 \times 10^{-12}$ s$^{-1}$ (one per 5,000 yr/cluster) assumes independence of ISL outage and coordinator failure. This independence assumption should be stated explicitly, as common-cause failures (e.g., solar events) could correlate both.

5. **Table II, collision avoidance rate:** $10^{-4}$/node/s yields ~8.6 events/node/day, which seems high. The footnote clarifies these are "screening notifications," but the distinction from autonomous maneuver commands should be made in the table itself.

6. **Figure references:** Several figures are referenced but cannot be evaluated (e.g., Fig. 3 fleet reuse, Fig. 6 unicast stagger). Ensure all figures have axis labels, units, and legends that are readable at column width.

7. **Section IV-E, $\eta_0$ audit:** The 0.5 pp gap explanation (coordinators don't send to themselves) is detailed but could be a footnote rather than body text.

8. **Abstract length:** At ~350 words, the abstract exceeds IEEE T-AES guidelines (typically 150–250 words). Consider condensing.

9. **"Project Dyson Research Team" authorship:** While the footnote explains this will be resolved for final publication, IEEE requires named authors at submission. This should be addressed before formal submission.

10. **Reference [52] (dyson_multimodel):** Self-referencing an unpublished methodology document for AI disclosure is acceptable, but the reference should note it is not peer-reviewed.

11. **Table III (bandwidth breakdown):** The "G.-S. Mesh" column shows ">1 kbps" total but the status reports alone are 205 bps. The $O(N)$ aggregation entry should show the actual value at $N = 10^5$ (which the text states is ~73 MB/node/cycle) to make the comparison meaningful.

12. **Slotted ALOHA fallback:** The claim that nominal operations survive Slotted ALOHA ($\gamma \approx 0.36$) at $\eta_{\text{total}} = 25.5\%$ is correct for throughput but ignores the collision-induced latency variability. A brief note on expected delay under ALOHA would be helpful.

---

## Overall Recommendation
**Recommendation: Major Revision**

This manuscript makes a legitimate contribution by assembling a systematic sizing framework for hierarchical coordination in large space swarms, filling a gap between swarm robotics (small scale) and constellation management (ground-controlled). The two-layer feasibility framework, the $\eta_0$/$\eta_{\text{cmd}}$ decomposition, the campaign duty factor, and the CCSDS-grounded $\gamma$ derivation are all valuable. The transparency of the verification hierarchy (Table IX) and the open-source commitment are exemplary.

However, the paper's central claims rest on a thin evidentiary base. The DES confirms its own equations; the packet-level simulator derives a parameter rather than validating the framework; the 363 ms margin at the recommended design point is uncomfortably small; and the GE channel model is illustrative rather than empirically grounded. The paper would be significantly strengthened by (a) a more honest framing of what the multi-tool verification actually demonstrates vs. what remains unvalidated, (b) a systematic margin analysis at the 30 kbps design point, and (c) reconciliation of the distributed planning overhead figures to extend the framework beyond centralized command generation.

The manuscript is also substantially too long for IEEE T-AES and would benefit from consolidation of sensitivity analyses into supplementary material. The core contribution—the two-layer feasibility framework with Algorithm 1—could be presented more concisely and with greater impact.

---

## Constructive Suggestions
*(Ordered by impact)*

1. **Conduct a systematic margin analysis** at 30 kbps: tabulate all unmodeled overheads with conservative estimates, compute the residual margin, and if necessary revise the minimum viable PHY rate. This directly affects the paper's primary design recommendation.

2. **Reconcile and integrate distributed planning overhead** (3.1% vs. 30.7%) into the feasibility framework with a worked example. This extends the framework's applicability to its stated target (autonomous swarms).

3. **Reframe the verification narrative** around what each tool uniquely contributes: analytical equations for parametric insight; DES for distributional characterization under stochastic campaigns; slot-sim for TDMA-specific interactions (ARQ coupling); packet-sim for standards-grounded parameter derivation. Drop the term "validation" for Tier 1.

4. **Reduce manuscript length by ~30%**: move FEC rate sensitivity, coherence-time sensitivity, and the detailed $\eta_0$ audit to supplementary material. The core framework (Sections IV-A, IV-B, IV-C, IV-E, IV-J, and Section V) can stand alone.

5. **Add a "practitioner's quick-start" subsection** that walks through Algorithm 1 with two worked examples at different scales (e.g., $N = 1{,}000$ at 10 kbps and $N = 50{,}000$ at 1 kbps) to demonstrate the framework's utility beyond the single instantiation presented.

6. **Strengthen the GE analysis** by identifying specific measurement opportunities and providing a simplified availability-based alternative for practitioners who lack GE parameters for their channel.

7. **Consider splitting into two papers**: (a) the sizing framework with analytical equations and Algorithm 1; (b) the TDMA schedulability analysis with slot-level and packet-level simulation. Each would be more focused and within page limits.