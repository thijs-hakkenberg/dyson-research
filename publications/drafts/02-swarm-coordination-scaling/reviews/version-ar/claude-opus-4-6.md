---
paper: "02-swarm-coordination-scaling"
version: "ar"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-27"
recommendation: "Major Revision"
---



# Peer Review: "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms"

## IEEE Transactions on Aerospace and Electronic Systems

---

## 1. Significance & Novelty

**Rating: 3 (Adequate)**

The paper addresses a genuine gap at the intersection of mega-constellation operations and swarm coordination: the lack of byte-level traffic accounting for hierarchical coordination architectures at the 10³–10⁵ node scale. The authors correctly identify that swarm robotics literature operates at 10–100 agents, constellation management at ~10⁴, and networking literature treats routing but not coordination overhead. The "design equations" framing—providing closed-form sizing rules for practitioners—is a useful contribution format for this community.

However, the novelty is more limited than the framing suggests. The core analytical results are relatively straightforward applications of existing theory: M/D/1 queueing (Kleinrock), geometric-distribution AoI (Kaul/Yates), and Gilbert-Elliott loss models. The "design equations" in Section V-C are essentially dimensional analysis of fixed message sizes divided by fixed bandwidth budgets. The headline result—that protocol overhead is O(1) in N for a hierarchical tree with fixed fan-out—follows directly from the topology definition (Eq. 4) and does not require simulation to establish. The 5%–46% overhead range is dominated by the workload assumption (whether commands are sent), not by any architectural insight.

The paper's strongest novelty claim is the joint-independence verification (Section IV-D), showing that GE loss and coordinator saturation compose independently under point-to-point ISLs. This is a useful practical finding, though the authors correctly note it is a property of the pipeline model rather than a general principle. The operating regime framing (RF-backup at <1% of time) is intellectually honest but raises the question of whether the entire analysis addresses a corner case of limited practical consequence.

## 2. Methodological Soundness

**Rating: 3 (Adequate)**

The simulation methodology is clearly described and the cycle-aggregated approach is appropriate for the message-layer analysis claimed. The vectorized implementation enabling ~7s runtimes at N=10⁵ is practical, and the 30 MC replications with bootstrap CIs are adequate for the low-variance metrics reported (SD < 0.001% for overhead). The validation against Pollaczek-Khinchine (within 2%) and gossip convergence bounds provides useful calibration.

**However, several methodological concerns arise:**

The simulation is essentially a deterministic byte-counting exercise with stochastic overlays (Bernoulli/GE loss, exponential failures). The extremely low variance (SD < 0.001%) confirms that the "simulation" is verifying arithmetic rather than exploring emergent behavior. When the DES matches the closed-form to within 0.1% at all fleet sizes (Table VII), one must ask what the simulation adds beyond the closed-form equations themselves. The authors partially address this in Section I-D (joint-condition verification), but the joint interaction test (Table V) also shows minimal interaction—precisely because the pipeline stages are independent by construction.

The static cluster membership assumption is a significant limitation that the authors acknowledge (Section V-B) but understate. In LEO mega-constellations, cross-plane relative motion creates cluster re-association on ~90-minute timescales for inclined orbits. The claim that "co-moving elements in the same orbital shell change neighbor distances on timescales of hours to days" (Section III-B) is true only for co-planar satellites; Walker constellations with multiple planes would experience frequent topology changes. This is not a minor limitation—it potentially invalidates the fixed-topology overhead calculations for realistic constellation geometries.

The centralized baseline parameterization deserves scrutiny. Setting μ_s = 1,000 msg/s for a single server (yielding ρ = 1.0 at N = 10,000) creates an artificially weak baseline. The authors acknowledge this with the M/D/c extension (Table I), but the headline comparison in Fig. 8 uses the c=1 bound. The honest conclusion—that centralized processing doesn't diverge until N ≈ 10⁶ with realistic provisioning—somewhat undermines the motivation for hierarchical coordination, leaving fault tolerance and spectrum independence as the primary advantages. The authors state this clearly, which is commendable, but it weakens the paper's impact.

The collision avoidance rate of 10⁻⁴/node/s is described as "screening events, not maneuver-triggering" but the sensitivity analysis (±1.5 pp) suggests this parameter has minimal impact on results regardless. More concerning is the absence of any orbital mechanics—conjunction geometry, relative velocity distributions, and screening volume calculations would significantly affect the relevance of the coordination architecture to its stated application.

## 3. Validity & Logic

**Rating: 3 (Adequate)**

The analytical derivations are correct and the DES verification is thorough within its scope. The AoI geometric-distribution prediction (Eq. 6) matching the DES to within 1 second (441 vs. 440s) is a clean validation. The GE loss analysis correctly identifies the structural ineffectiveness of intra-cycle retransmission during correlated bursts (27.1% vs. 87.5% i.i.d.), and the inter-cycle recovery projection (4–7 cycles to 95%) is physically reasonable.

The logical structure of the argument is generally sound, but several interpretive issues arise. First, the paper frames the 9× overhead envelope (5%–46%) as a key finding, but this is entirely driven by the binary choice of whether to send 512-byte commands to every node every cycle. This is a workload assumption, not an architectural property. The decomposition in Fig. 5 confirms that commands account for >60% of stress-case traffic—meaning the "hierarchical coordination overhead" is mostly "command dissemination overhead" that would exist in any topology.

Second, the sectorized mesh comparison (Section III-B.4) uses a √N heuristic for sector size that is described as "an order-of-magnitude heuristic." The 1.4–1.5× overhead ratio relative to hierarchical is presented as a meaningful comparison, but the sensitivity to the neighbor cap (Table IV) shows that the sectorized mesh overhead varies from 62% to >100% depending on a single parameter choice. This makes the comparison fragile.

Third, the inter-cycle store-and-forward recovery analysis (end of Section IV-C) is explicitly noted as "analytical extrapolation, not the DES." This is appropriate disclosure, but it means one of the four primary contributions (correlated loss recovery) is not validated by the simulation tool that is the paper's other primary contribution. The 4–7 cycle recovery estimate assumes independent state transitions between cycles, which may not hold for physical phenomena (e.g., solar particle events lasting hours).

The paper is commendably honest about limitations. The explicit statements that joint independence "would not hold under shared-medium RF contention," that the centralized baseline "does not diverge computationally until N ≈ 10⁶," and that results are "message-layer estimates" all demonstrate intellectual rigor. However, this honesty accumulates into a concern: after all caveats are applied, the practical design guidance may be too hedged to be actionable.

## 4. Clarity & Structure

**Rating: 4 (Good)**

The paper is well-organized with a clear roadmap (beginning of Section IV) and consistent notation throughout. The practitioner-oriented framing—design equations collected in Section V-C, sizing tables, and explicit parameter tables—is effective for the target audience. The distinction between offered and delivered overhead, and between message-layer and MAC-layer estimates, is carefully maintained.

Tables are generally well-constructed and informative. Table VI (Traffic Accounting) is particularly useful for reproducibility. The consistent use of footnotes to qualify assumptions (e.g., Table VII footnotes on SD and effective overhead) adds precision without cluttering the main text. The abstraction scope table (Table III) is an excellent practice that more simulation papers should adopt.

Several clarity issues should be addressed. The abstract is dense to the point of being difficult to parse on first reading—it attempts to convey too many specific numbers (21–50 kbps, P99=440s, 27%, 4–7 cycles, 9×, etc.) without sufficient context. A more narrative abstract would better serve readers. The paper length is substantial (~12 pages of dense technical content) and could benefit from consolidation; for example, the sectorized mesh analysis (Section III-B.4) and neighbor-cap sensitivity (Table IV) could be shortened without loss of key findings.

The notation is mostly consistent but the overloading of η (offered vs. delivered, with and without baseline, effective vs. message-layer) creates occasional confusion despite the careful definitions. The relationship between C_node (1 kbps per-node budget), C_coord (21–50 kbps coordinator ingress), and the physical transceiver rate could be clarified earlier—the explanation in Section III-F is important but comes late.

Figures are referenced but provided as PDF placeholders; I cannot evaluate their quality. Based on captions, they appear appropriate and well-described.

## 5. Ethical Compliance

**Rating: 4 (Good)**

The paper includes an explicit AI-assistance disclosure in the Acknowledgment section, noting that "Claude 4.6, Gemini 3 Pro, GPT-5.2" were used for "AI-assisted ideation" that "motivated aspects of the coordinator architecture but is not validated here." This is transparent and appropriate. The reference to a separate methodology paper [47] provides additional context.

The open-source code availability (GitHub with tagged release) and full parameter disclosure (Table II) support reproducibility. The "Data Availability" section is thorough.

The anonymous authorship ("Project Dyson Research Team") with a note that "Individual author names and affiliations will be provided for final publication per IEEE policy" is unusual but not unprecedented for pre-publication manuscripts. IEEE policy requires named authors for publication; this should be resolved before acceptance.

One minor concern: the paper references model versions (Claude 4.6, GPT-5.2) that do not exist as of my knowledge cutoff. If these are speculative/fictional model names, this should be clarified; if the paper is set in a near-future context, this is unconventional for a technical journal submission.

## 6. Scope & Referencing

**Rating: 3 (Adequate)**

The paper is appropriate for IEEE TAES in its treatment of space systems coordination, though it sits at the boundary between aerospace systems and computer networking. The queueing theory and gossip protocol analysis would also fit IEEE Transactions on Networking or IEEE JSAC.

The reference list (50 items) covers the major relevant areas: constellation operations (Starlink, Kuiper, OneWeb), distributed systems theory (Lamport, Raft, Lynch), swarm robotics (Brambilla, Dorigo), AoI (Kaul, Yates, Kadota), and queueing theory (Kleinrock). However, several gaps exist:

- **No references to actual ISL implementations or measurements.** The paper assumes 1–10 Gbps optical ISLs but cites no experimental or operational data on ISL performance, availability, or failure modes. Starlink's operational ISL experience would be highly relevant.
- **Missing recent work on distributed space systems.** The CCSDS DTN reference is from 2007 (RFC 4838); more recent work on space networking protocols (e.g., Consultative Committee publications post-2020, ESA's OPS-SAT experiments) is absent.
- **No references to actual conjunction assessment operations.** The paper's primary application is coordination for collision avoidance, but it cites only Alfano [50] for conjunction probability and ESA [49] for space environment statistics. The 18th Space Defense Squadron's operational conjunction assessment process, and recent work on autonomous collision avoidance (e.g., ESA's CREAM system), would strengthen the application context.
- **Several references are non-archival** (Amazon website, DARPA program pages, DoD fact sheets). While acknowledged with "(non-archival)" tags, these weaken the scholarly foundation. The Starlink reference [1] is an FCC filing supplemented by a personal website—adequate but not ideal.

The related work section (Section II) is organized but somewhat superficial. The treatment of mean-field games [38,39] and GNN controllers [36,41] as relevant prior work is a stretch—these address fundamentally different problems (continuous-state consensus and learned policies) than byte-level traffic accounting.

---

## Major Issues

1. **The simulation adds minimal value beyond the closed-form equations.** The DES matches analytical predictions to within 0.1% at all scales (Table VII), and the joint-interaction test (Table V) confirms independence that is obvious from the pipeline architecture. The paper should either (a) identify scenarios where the DES reveals behavior not predicted by the closed-form (e.g., transient overloads, cascading failures, dynamic cluster re-association), or (b) reframe the contribution as primarily analytical with the DES as a verification tool rather than a co-equal contribution.

2. **Static topology assumption invalidates results for realistic LEO constellations.** The paper acknowledges this limitation but does not quantify the impact. For a Walker constellation with multiple orbital planes (e.g., Starlink's 72 planes at 53° inclination), cross-plane relative velocities of ~15 km/s create topology changes on orbital-period timescales. The overhead of cluster re-association (state transfer, coordinator re-election) could dominate the steady-state overhead that the paper analyzes. At minimum, an analytical estimate of re-association frequency and overhead for representative constellation geometries should be provided.

3. **The inter-cycle recovery analysis (a primary contribution) is not validated by the DES.** The paper explicitly states this is "analytical extrapolation, not the DES" and lists DES implementation as "future work." For a paper whose stated contribution includes an "open-source cycle-aggregated simulation," having one of four primary results be purely analytical is a significant gap. Either implement cross-cycle retry in the DES or downgrade this from a primary contribution.

4. **The practical relevance of the RF-backup operating regime is unclear.** The paper states this regime represents <1% of operational time, and that under nominal optical ISLs "coordination overhead is negligible." The entire analysis thus characterizes a rare degraded mode. While designing for degraded modes is important, the paper should more clearly articulate the operational scenarios (e.g., solar storm duration, optical ISL MTBF) that determine how often and how long this regime is encountered, and whether the 1 kbps budget is the binding constraint during those periods.

5. **Absence of any orbital mechanics modeling.** For a paper targeting IEEE TAES and claiming relevance to mega-constellation coordination, the complete absence of orbital mechanics is a significant gap. Cluster geometry, conjunction screening volumes, relative motion within and between clusters, and Earth-occlusion patterns all affect the coordination architecture's performance. The 500 km cluster diameter and 10s coordination cycle are assumed without orbital justification.

---

## Minor Issues

1. **Abstract (lines 1–15):** Too many specific numbers without context. Consider leading with the problem and approach before presenting numerical results.

2. **Eq. 2:** The M/D/1 waiting time formula $W_q = \rho / [2\mu_s(1-\rho)]$ is correct but should note this is the Pollaczek-Khinchine result for deterministic service, not the general M/G/1 formula.

3. **Section III-B.2, coordinator handoff:** The "seed handoff" concept (2 kB in 16s at 1 kbps) for RF-only emergency re-election is interesting but the claim that this enables meaningful coordination recovery needs justification. What state can a new coordinator reconstruct from a cluster index, random seed, and member roster?

4. **Table II:** The collision avoidance rate footnote marker "a" is defined but footnote "b" is missing (jumps from "a" to "c" to "d").

5. **Section III-F:** The statement "effective utilization (74–84%) exceeds Slotted ALOHA capacity, confirming TDMA is required" conflates offered load with throughput capacity. Slotted ALOHA's maximum throughput is 1/e ≈ 36.8%, not a utilization threshold.

6. **Table V (Joint Interaction):** The "GE Only" column shows identical drops to "No Loss" at every capacity level. This is because GE losses occur before coordinator ingress (as explained in the text), but the table presentation is confusing—it appears GE has zero effect, which is true for drops but not for delivered throughput.

7. **Section IV-B:** The AoI-to-position-error coupling (441s → ~230m at 0.5 m/s drift rate) uses a linear extrapolation that ignores orbital mechanics. Along-track position uncertainty grows nonlinearly due to differential drag and gravitational perturbations; 441s of unmodeled propagation could yield significantly larger errors depending on atmospheric conditions.

8. **Eq. 5 (mesh messages):** The notation $f = O(N/\log N)$ is unusual—fanout is typically a design parameter, not an asymptotic quantity. Clarify whether this is a specific choice or a scaling relationship.

9. **Section V-C (Design Equations Summary):** The "safe-mode floor" equation $\gamma_{\min} = \eta / 1.0$ is trivially $\gamma_{\min} = \eta$. The denominator of 1.0 adds no information.

10. **References:** [47] (dyson_multimodel) is a self-citation to a URL with no publication venue, date, or verification of availability. This should be either published or removed.

11. **Acknowledgment:** "Total MC wall-clock time: ~90 min on commodity hardware" is useful but should specify the hardware (CPU, RAM) for reproducibility.

12. **Throughout:** The paper uses "~" (tilde) inconsistently for approximate values—sometimes ${\sim}5\%$, sometimes $\approx 5\%$. Standardize.

---

## Overall Recommendation

**Major Revision**

The paper addresses a legitimate gap in the literature and provides a well-organized, transparent analysis of hierarchical coordination overhead for large space swarms. The practitioner-oriented design equations and open-source simulation are valuable contributions in principle. However, the paper suffers from a fundamental tension: the analytical results are straightforward enough that the simulation adds minimal insight, while the simulation is too abstract (no orbital mechanics, static topology, message-layer only) to provide the physical-layer grounding needed for practical design guidance. The static topology assumption, unvalidated inter-cycle recovery analysis, and narrow operating regime (RF-backup at <1% of time) collectively limit the paper's impact. A major revision should address the topology dynamics gap (at minimum analytically), validate the inter-cycle recovery in the DES, and either strengthen the simulation's role through more complex scenarios or reframe the contribution as primarily analytical.

---

## Constructive Suggestions

1. **Add a representative orbital geometry case study.** Select one concrete constellation (e.g., a Walker delta 53°/72/1 at 550 km, approximating Starlink) and compute: (a) cluster re-association frequency for co-planar vs. cross-plane clusters; (b) Earth-occlusion statistics for ISLs; (c) conjunction screening volume and expected screening events per cluster per cycle. This would ground the abstract message-layer analysis in physical reality and is achievable analytically without modifying the DES.

2. **Implement cross-cycle retry in the DES.** This is listed as future work but is essential for validating the GE recovery contribution. The analytical model assumes independent state transitions; the DES could reveal whether burst durations (which are geometrically distributed in the GE model) create longer recovery tails than predicted. This would also give the simulation a result that the closed-form cannot easily provide.

3. **Reframe the simulation contribution around joint/emergent behavior.** The DES's value is not in verifying O(1) overhead (which is trivial from the topology) but in testing conditions where single-factor equations might fail. Design scenarios with: (a) correlated coordinator failures (SPE affecting an orbital plane); (b) dynamic cluster re-association under orbit-raising; (c) simultaneous GE bursts across multiple clusters. These would demonstrate the simulation's value beyond arithmetic verification.

4. **Sharpen the comparison with centralized architectures.** Since the paper honestly acknowledges that centralized processing scales to 10⁶, quantify the specific scenarios where hierarchical coordination provides operational advantage: ground station outage duration and frequency, uplink spectrum contention at N=10⁵, and the probability of needing autonomous coordination during the <1% RF-backup period. This would transform the vague "fault tolerance advantage" into a quantified availability improvement.

5. **Reduce paper length by 15–20%.** The sectorized mesh analysis, while interesting, could be condensed to a single paragraph and table. The extensive footnotes in tables (some running 4–5 lines) should be integrated into the text or shortened. The repeated statements about MAC overhead scaling by 1/γ (appearing in the abstract, Section I-D, Section III-F, Section V-C, and Section VI) could be stated once with a forward reference.