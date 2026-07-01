---
paper: "02-swarm-coordination-scaling"
version: "bi"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-27"
recommendation: "Major Revision"
---



# Peer Review: "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms"

**Manuscript Version:** BI
**Venue:** IEEE Transactions on Aerospace and Electronic Systems

---

## 1. Significance & Novelty

**Rating: 3 (Adequate)**

The paper addresses a genuine gap: the absence of closed-form parametric sizing relationships for coordination architectures at the $10^3$–$10^5$ node scale with byte-level traffic accounting. This is a practically relevant problem as mega-constellations grow beyond current operational experience. The claim in Section I-A that "no prior work provides closed-form parametric sizing relationships for coordination architectures across $10^3$–$10^5$ nodes with byte-level traffic accounting under a fixed per-node budget" is plausible, though the authors should more carefully distinguish their contribution from existing CCSDS link budget methodologies and constellation design handbooks (e.g., SMAD Chapter 13) that perform similar per-link accounting at smaller scales.

However, the novelty is tempered by the nature of the results. The core finding—that architecture-specific overhead is ~5% and command traffic dominates—is essentially a consequence of the message model assumptions rather than a deep structural insight. The $O(N)$ scaling of the hierarchical architecture is well-known from tree-structured aggregation; the contribution is in parameterizing the constants. The design equations themselves (Section V-C) are relatively straightforward: the overhead equation is a linear sum of message sizes divided by the bandwidth-time product, the AoI expression follows directly from geometric inter-arrival times, and the coordinator ingress sizing is a basic capacity calculation. While packaging these into a coherent "practitioner toolkit" has value, the intellectual depth is modest for a top-tier transactions journal.

The GE inter-cycle recovery analysis (Section IV-C) and the parametric design curves (Fig. 5) represent the most novel analytical contribution, providing useful design guidance across channel burstiness regimes. The explicit acknowledgment that the GE model is inappropriate for deterministic Earth occultation (a common oversight in the literature) is commendable.

## 2. Methodological Soundness

**Rating: 3 (Adequate)**

The methodology has a fundamental structural issue that the authors partially acknowledge but do not fully resolve: the DES operates at the same abstraction level as the closed-form equations, so the claimed "verification" (agreement <0.1%) is essentially checking arithmetic consistency rather than validating the model against reality. The paper is transparent about this (Section III-A: "Both operate at the same message-layer abstraction; physical-layer validation is future work"), but the framing throughout sometimes overstates what has been demonstrated. For instance, the abstract's "An open-source Monte Carlo tool verifies implementation consistency to <0.1%" is accurate, but the casual reader may interpret this as stronger validation than it is.

The statistical methodology is generally sound. The 30 MC replications with bootstrap CIs are appropriate, and the per-run-then-aggregate approach for tail statistics (Table V footnote) correctly avoids inflated confidence from pooling correlated samples. However, the SD < 0.001% for overhead (Section III-D) raises a question: if the DES implements the same deterministic byte-counting as the closed-form equations, near-zero variance is expected by construction, not a meaningful validation metric. The variance should come from stochastic elements (failures, GE transitions, collision events), and the paper should report these separately.

The assumption of static cluster membership for one year (Section III-B.2) is a significant simplification for LEO constellations. While the authors bound the re-association overhead at <0.5% (Section V-B), this analysis considers only the bandwidth cost and not the transient coordination quality degradation during handoffs. The quantitative bound in Section V-B ($f_h = 0.8\%$) is helpful but assumes a single re-association rate; in practice, nodes near orbital-plane intersections experience much higher rates, and the fleet-average masks this heterogeneity.

The coordinator failure transient analysis (Section III-B.2) is thorough, covering both optical and RF-backup scenarios. However, the double-fault scenario (coordinator failure concurrent with optical outage) deserves more rigorous treatment—the claim that "these events may be correlated" understates the issue for power-negative failure modes where optical ISL loss is virtually certain.

## 3. Validity & Logic

**Rating: 3 (Adequate)**

The internal logic of the paper is generally sound, and the authors are commendably careful about qualifying their claims. The distinction between architecture-specific overhead (~5%) and workload-dependent overhead (up to 46%) is well-drawn and important. The observation that command traffic is topology-invariant "given the assumed workload semantics" (Section I-C) is a crucial qualifier that is appropriately repeated.

However, several logical issues deserve attention:

**The 1 kbps design point.** The paper devotes enormous attention to the 1 kbps RF-backup regime while acknowledging it applies <1% of operational time (Section III-E). Table II shows that at ≥10 kbps, essentially all the interesting design challenges vanish. This creates a tension: either the 1 kbps case is the design-driving edge case (as argued), in which case the paper should more thoroughly analyze the degraded-mode operations it enables, or it is a corner case that receives disproportionate attention. The argument that it "determines whether coordination survives ISL disruption" is valid but could be made more concisely.

**The sectorized mesh comparison.** The paper correctly notes that the sectorized mesh provides different functional scope (Table IX), but then repeatedly compares overhead figures (e.g., "14× difference in bandwidth efficiency per unit of awareness"). This normalized metric is misleading because the two architectures serve fundamentally different purposes—the hierarchy provides command dissemination and fleet-wide aggregation that the mesh does not. The comparison would be more informative if restricted to the common functional subset (local neighbor monitoring).

**Schedulability of stress-case unicast.** The 22-cycle stagger requirement (Eq. 9, Table VII) means that under stress-case unicast, each node receives its unique command only every 220 seconds on average. This is a significant operational constraint that is mentioned but not adequately discussed in terms of mission impact. What operations require per-node unicast commands at every-cycle cadence? If the answer is "very few," the stress case may be unrealistically conservative; if "many," the 22-cycle latency is a serious limitation.

**AoI operational relevance.** The coupling to conjunction screening (Section IV-B) is well-argued for the P99 = 441 s case. However, the paper does not address whether the exception telemetry model ($p_{\text{exc}} = 0.10$) is operationally realistic. What triggers an exception? If it is threshold-based on state deviation, the probability depends on orbital dynamics, not a fixed parameter. This coupling is identified as future work but weakens the current AoI results.

## 4. Clarity & Structure

**Rating: 3 (Adequate)**

The paper is dense but generally well-organized. The roadmap at the beginning of Section IV is helpful. The notation table (Table I) is a good practice. The design equations summary (Section V-C) serves the stated goal of a "practitioner toolkit."

However, the paper suffers from several clarity issues:

**Length and repetition.** The manuscript is extremely long for a journal paper (I estimate ~12,000 words plus extensive tables and figures). Key results are stated multiple times: the ~5% architecture-specific overhead appears in the abstract, Section I-C (twice), Section IV-E, Section V-C, and Section VI. The 46% stress-case figure appears even more frequently. While some repetition aids comprehension, this level suggests the paper could be significantly condensed.

**Notation overload.** The paper introduces many symbols ($\eta$, $\eta_0$, $\eta_E$, $\eta_S$, $\eta_{\text{total}}$, $\eta_{\text{eff}}$, $\eta_{\text{sector}}$, $\eta_{\text{sync}}$) that are closely related but subtly different. The distinction between $\eta$ (protocol overhead beyond baseline) and $\eta_{\text{total}}$ ($= \eta + 20.5\%$) requires constant mental bookkeeping. A clearer visual framework (perhaps a stacked bar chart showing the composition) would help.

**Figure quality cannot be assessed** since figures are referenced but not provided (PDF format). The captions are informative, which is good practice.

**The abstract** is accurate but overloaded with specific numbers. A more concise abstract focusing on the key insight (architecture-specific overhead is small; command traffic dominates; coordinator ingress is the binding constraint at low bandwidth) would be more effective.

**Section III-B.2** (Hierarchical Topology) is particularly dense, mixing the topology description with coordinator failure analysis, Raft election details, and RF-backup handoff timing. This should be restructured—perhaps separating the nominal architecture description from the failure/recovery analysis.

## 5. Ethical Compliance

**Rating: 4 (Good)**

The paper includes an appropriate acknowledgment of AI-assisted ideation (Acknowledgment section), citing specific models and noting that the AI contributions "are not validated here." This is transparent and responsible. The open-source code availability (with specific tag) supports reproducibility. The anonymous authorship ("Project Dyson Research Team") with a note about final publication is acceptable for review but must be resolved for publication per IEEE policy.

One minor concern: the reference to "Claude 4.6, Gemini 3 Pro, GPT-5.2" suggests future model versions that do not exist as of the review date. If these are hypothetical or the paper is set in a near-future context, this should be clarified to avoid confusion. If the paper was actually written with current-generation AI assistance, the specific models used should be accurately named.

## 6. Scope & Referencing

**Rating: 3 (Adequate)**

The paper is appropriate for IEEE T-AES in scope, addressing autonomous spacecraft coordination at scale. The reference list is comprehensive (50+ references) and covers the relevant domains: constellation operations, swarm robotics, distributed systems theory, queueing theory, and space standards.

However, several gaps exist:

- **No references to actual ISL link budget analyses** for LEO constellations. The 1 kbps and 24 kbps figures should be grounded in published link budgets (e.g., from CCSDS or published Starlink/Iridium analyses).
- **Missing references on space-based TDMA implementations.** The TDMA frame analysis (Section IV-A) would benefit from citing actual space TDMA systems (e.g., TDRSS MA return, or ESA's EDRS scheduling).
- **No reference to the DTN/CGR literature** beyond the basic RFC 4838. Contact Graph Routing (Fraire et al., 2021) is directly relevant to scheduled communication in LEO constellations with predictable contact windows.
- Several references are non-archival (Amazon website, DARPA program pages, DoD fact sheets). While understandable for program descriptions, the paper relies on these for factual claims about operational scale that should be supported by peer-reviewed sources where possible.
- The self-citation [dyson_multimodel] appears to be an unpublished working paper; its status should be clarified.

---

## Major Issues

1. **Validation gap is more serious than acknowledged.** The DES and closed-form equations operate at identical abstraction levels, making the <0.1% agreement a tautological consistency check rather than validation. The paper needs either (a) a packet-level simulation of at least one cluster to demonstrate that message-layer abstractions hold, or (b) a much more prominent and explicit framing of results as *analytical predictions pending physical-layer validation*, with a quantitative error budget for the abstracted phenomena (MAC contention, link acquisition delays, Doppler effects). Currently, the paper oscillates between these framings.

2. **The workload model is assumed, not derived.** The entire overhead analysis depends on message sizes (256 B status, 512 B commands, 64 B heartbeats) and rates ($r = 0.1$ msg/s, $p_{\text{exc}} = 0.10$) that are stated as parameters but not justified from operational requirements. The paper should either (a) derive these from a specific mission scenario (e.g., conjunction screening cadence → required state update rate → message size), or (b) present a more systematic sensitivity analysis showing how results change across the full parameter space, not just the three workload profiles.

3. **The comparison framework is structurally unfair.** The centralized baseline models only compute-queue scalability (no communication overhead), the global-state mesh is an intentional worst case, and the sectorized mesh provides different functionality. This means the hierarchical architecture is never compared against a peer architecture providing equivalent functionality at equivalent abstraction depth. The paper should either (a) implement a communication-layer model for the centralized case (including uplink scheduling and ground contact constraints) or (b) restrict claims to "the hierarchical architecture fits within a 1 kbps budget" without comparative superiority claims.

4. **Missing analysis of correlated/cascading failures.** The paper assumes i.i.d. exponential node failures (Section III-C) but acknowledges correlated failure modes (SPE, batch defects) only as future work (Section V-B). For a system claiming to operate at $10^5$ nodes, correlated failures are not an edge case—they are a design-driving scenario. A solar particle event could simultaneously degrade hundreds of nodes. At minimum, a sensitivity analysis showing how the architecture degrades under correlated failures (e.g., 5% simultaneous coordinator failures) is needed.

---

## Minor Issues

1. **Eq. (2):** The M/D/1 waiting time formula $W_q = \rho / (2\mu_s(1-\rho))$ is the standard result but should note it assumes FCFS discipline and Poisson arrivals; the deterministic service time gives the factor of 2 reduction vs. M/M/1.

2. **Table III (Simulation Parameters):** The collision avoidance rate footnote says "Screening events, not maneuver-triggering" but the sensitivity range ($10^{-5}$ to $10^{-3}$) spans three orders of magnitude. The baseline $10^{-4}$/node/s yields ~8.6 events/node/day, which seems high even for screening. Please justify against published conjunction statistics (e.g., ESA's annual report [esa_space_env]).

3. **Section III-B.4 (Sectorized Mesh):** The $\sqrt{N}$ sector sizing is described as "an order-of-magnitude heuristic" based on orbital density arguments. This should be more rigorously justified or clearly flagged as a modeling choice rather than a derived result.

4. **Eq. (7):** The AoI P99 formula uses $\lceil \cdot \rceil$ (ceiling), which is correct for discrete cycles, but the text says "matching the DES value of 441 s" while the formula gives exactly 440 s. The 1 s discrepancy likely comes from the ceiling vs. continuous approximation; clarify.

5. **Table VI (Joint Interaction):** The "No Loss" and "GE Only" columns are identical, which is the paper's point about pipeline decoupling. However, this is true *by construction* under dedicated links—it would be more informative to show what happens under shared-medium access where the decoupling breaks.

6. **Section IV-A, TDMA synchronization:** The claim that "TCXO (~1 ppm) maintains <0.6 ms drift over 10 min" should be verified: 1 ppm × 600 s = 0.6 ms. This is correct but assumes the TCXO is calibrated at the start of the outage; long-term aging effects could be significant.

7. **Table IV (AoI Results):** The "Periodic baseline" row shows Mean AoI = 4.9 s, which should be exactly $T_c/2 = 5.0$ s for uniform sampling within a cycle. The 0.1 s discrepancy should be explained (likely processing delay).

8. **Formatting:** The paper uses both "kbps" and "kB" without consistently defining whether "k" is $10^3$ or $2^{10}$. For a byte-level accounting paper, this matters.

9. **Section III-B.2:** The RF-backup handoff analysis mentions "Slotted ALOHA" for Raft election messages, but the rest of the paper assumes TDMA. Clarify whether Slotted ALOHA is used only during the election phase (before a coordinator establishes the TDMA schedule).

10. **Bibliography:** Reference [1] cites both an FCC filing and a non-archival website (planet4589.org) in the same entry. These should be separate references.

---

## Overall Recommendation

**Major Revision**

The paper addresses a relevant problem and provides a useful analytical framework for sizing hierarchical coordination architectures. The design equations, while individually straightforward, are packaged into a coherent toolkit with appropriate sensitivity analysis and cross-checks. The GE recovery analysis and parametric design curves are genuinely useful contributions. However, the paper has significant issues that prevent acceptance in its current form: (1) the validation claim is overstated given that the DES and equations operate at the same abstraction level; (2) the comparison framework is structurally asymmetric; (3) the workload model is assumed rather than derived; and (4) correlated failure analysis is absent despite being critical at the target scale. The paper is also substantially too long and would benefit from significant condensation. With a major revision addressing these issues—particularly adding at least a single-cluster packet-level validation and a correlated failure sensitivity analysis—the paper could make a solid contribution to the literature.

---

## Constructive Suggestions

1. **Add a packet-level validation of one cluster.** Implement a single cluster ($k_c = 100$) in NS-3 or MATLAB with the TDMA frame from Table V, including preamble detection, CRC failures, half-duplex turnaround, and realistic propagation. Compare the message delivery rate and AoI against the analytical predictions. Even a single-cluster validation would dramatically strengthen the paper's claims and is explicitly identified as the "recommended next validation step" (Section V-A). This is the single highest-impact improvement.

2. **Derive the workload model from a specific mission scenario.** Choose one concrete use case (e.g., conjunction screening for a 550 km shell constellation) and derive message sizes and rates from operational requirements: required state accuracy → update cadence → message content → byte count. This grounds the analysis in physical reality rather than assumed parameters and makes the toolkit immediately applicable.

3. **Condense the paper by ~30%.** The key results can be communicated in roughly 8–9 pages rather than the current ~13+. Specific targets: merge the three workload profiles into a single parameterized equation (already done in Section V-C); move the sectorized mesh sensitivity (Table III-B.4) to an appendix; reduce the TDMA frame analysis to the essential result (24 kbps, 623 ms margin) with derivation details in supplementary material; eliminate redundant restatements of the 5%/46% finding.

4. **Add a correlated failure sensitivity analysis.** Simulate a scenario where 5–10% of coordinators fail simultaneously (modeling a solar particle event or batch hardware defect). Report the fraction of nodes that lose coordination, the recovery time, and the AoI impact. This would address the most significant gap in the failure analysis and is straightforward to implement in the existing DES.

5. **Reframe the topology comparison honestly.** Either implement communication-layer overhead for the centralized case (including ground contact scheduling and uplink contention) to enable a fair comparison, or explicitly restrict the paper's claims to "the hierarchical architecture is feasible within a 1 kbps budget" without comparative superiority claims against architectures modeled at different abstraction levels. The current framing—with intentional bounds and different functional scopes—is technically correct but risks misleading readers who skim the results.