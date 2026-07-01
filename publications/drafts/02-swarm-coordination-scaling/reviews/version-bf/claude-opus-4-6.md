---
paper: "02-swarm-coordination-scaling"
version: "bf"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-27"
recommendation: "Major Revision"
---

# Peer Review: "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms"

**Manuscript Version:** BF
**Venue:** IEEE Transactions on Aerospace and Electronic Systems

---

## 1. Significance & Novelty

**Rating: 3 (Adequate)**

The paper addresses a genuine gap: there is no published, unified set of closed-form sizing equations for hierarchical coordination architectures spanning $10^3$–$10^5$ autonomous spacecraft nodes with byte-level traffic accounting. The authors correctly identify that swarm robotics literature operates at 10–100 agents, constellation management at ~$10^4$, and networking literature treats routing but not coordination protocol sizing. Assembling these relationships into a "practitioner toolkit" has practical value for the mega-constellation community.

However, the novelty is more integrative than fundamental. The individual analytical components—M/D/1 queueing, Gilbert-Elliott channel models, geometric AoI distributions, gossip convergence bounds—are all well-established. The paper's contribution is their assembly and parameterization for a specific four-level architecture. This is useful engineering work, but the intellectual contribution is closer to a design handbook chapter than a research advance. The central finding that "architecture-specific overhead is ~5%; commands dominate" is intuitive once the message model is specified—commands are 512 B vs. 64 B heartbeats and ~4 B amortized summaries, so of course they dominate.

The paper would be significantly strengthened if it derived non-obvious design insights that could not be anticipated from the individual component models. For instance, the joint interaction verification (Section IV-D) showing pipeline decoupling is a genuinely useful result, but it is presented as a verification rather than a design principle. The GE parameter sensitivity curves (Fig. 5b) providing design lookup for arbitrary burstiness are the most novel contribution and deserve more prominence.

## 2. Methodological Soundness

**Rating: 3 (Adequate)**

The analytical framework is internally consistent and the mathematics is correct as far as I can verify. The closed-form equations are standard results applied to the specific message model. The Monte Carlo configuration (30 replications, bootstrap CIs, per-run-then-aggregate tail statistics) is methodologically appropriate. The authors are commendably transparent about what the DES does and does not validate—it checks "implementation consistency, not physical fidelity."

However, this transparency also exposes the fundamental methodological limitation: the DES and the closed-form equations operate at the same abstraction level. When the authors report "<0.1% agreement," this confirms arithmetic consistency, not model validity. The paper essentially validates that two implementations of the same equations produce the same numbers. While useful for catching implementation bugs, this does not constitute the kind of independent validation that would support the design equations' use in practice. The authors acknowledge this (Section V-A), but the paper's framing sometimes overstates what has been demonstrated.

Several specific methodological concerns arise. First, the 1 kbps per-node budget is described as an "RF-backup regime" active <1% of operational time, yet the entire paper's analysis is conducted at this budget. The relevance to operational design is therefore narrow—Table II shows that at ≥10 kbps, most of the paper's results become trivially satisfied. Second, the static topology assumption is problematic for LEO cross-plane configurations where cluster membership changes on 45–90 minute timescales. The claimed <0.5% re-association overhead is asserted but not modeled. Third, the collision avoidance rate of $10^{-4}$/node/s is described as "screening events, not maneuvers," but the paper does not model the actual conjunction assessment workflow that would drive coordination traffic in practice. Fourth, the GE model's per-cycle coherence assumption (state constant within $T_c = 10$ s) is a strong simplification. While the authors argue it is conservative for recovery, it eliminates the possibility of modeling partial intra-cycle recovery that would occur with shorter coherence times, making the intra-cycle retry analysis somewhat circular.

## 3. Validity & Logic

**Rating: 3 (Adequate)**

The conclusions are logically supported within the stated assumptions, and the authors are generally careful about qualifying their claims. The distinction between architecture-specific overhead (~5%) and workload-dependent overhead (~46%) is well-drawn and important. The identification that commands are topology-invariant and dominate stress-case traffic is a valid and useful observation.

Several logical issues merit attention. The stress-case workload ($\eta \approx 46\%$) assumes one 512 B command per node per cycle, but Eq. (12) shows this requires 22 cycles to deliver via unicast at 24 kbps half-duplex. The paper correctly identifies this but then continues to use $\eta \approx 46\%$ as a primary metric throughout. This creates confusion: is 46% a meaningful design point or an infeasible upper bound? The event-driven profile ($\eta \approx 6\%$) is described as "operationally representative," yet receives far less analytical attention. The paper would be more coherent if it centered on the event-driven profile and treated the stress case as a boundary check.

The topology comparison (Table VII, Fig. 8) has a significant apples-to-oranges problem that the authors partially acknowledge but do not fully resolve. The hierarchical architecture provides full cluster awareness (100 nodes), while the capped sectorized mesh provides local awareness of ~10 neighbors. Comparing their overhead ratios (46% vs. 65–67%) without normalizing for service scope is misleading despite the caveats in Table IX. The centralized baseline models only compute-queue scalability, not communication overhead, making cross-architecture comparison incomplete. The authors note this in footnote (d) of Table VII, but the figures (Fig. 8) still plot all four topologies on the same axes, inviting direct comparison.

The AoI analysis correctly derives the geometric distribution result (Eq. 8), but the practical interpretation is underdeveloped. A P99 AoI of 441 s at $p_{\text{exc}} = 0.10$ corresponds to ~230 m along-track uncertainty—the authors note this is "a coarse screening value, not a navigation input," but do not discuss whether this is acceptable for the coordination functions the architecture is supposed to support. Without coupling to mission requirements, the AoI numbers are descriptive but not prescriptive.

## 4. Clarity & Structure

**Rating: 3 (Adequate)**

The paper is dense but generally well-organized. The roadmap at the beginning of Section IV is helpful. The notation table (Table I) is a good practice. The design equations summary in Section V-C is valuable for practitioners.

However, the paper suffers from significant length and complexity issues that impair readability. At approximately 12,000 words of body text plus extensive tables and figures, it substantially exceeds typical IEEE T-AES length. The presentation is heavily front-loaded with caveats, qualifications, and cross-references that, while individually justified, collectively make the paper difficult to follow on first reading. For example, the coordinator bandwidth discussion in Section IV-A presents three models (A, B, TDMA), then discusses half-duplex partitioning, then command dissemination types, then TDMA frame feasibility, then synchronization, then guard-time sensitivity—all before the reader has a clear picture of the primary result (coordinator needs ~24 kbps under TDMA).

The abstract is accurate but reads more like a technical summary than an abstract—it includes too many specific numbers (21–25 kbps, 440 s, 4 cycles, 22-cycle scheduling) without sufficient context for a reader encountering the paper for the first time. The parenthetical qualifications ("parametric design curves; no measured channel statistics assumed") belong in the body.

Several figures are referenced but provided as PDF placeholders (e.g., `fig-architecture-diagram.pdf`), so I cannot evaluate their quality. The tables are generally well-constructed, though Table IV (simulation parameters) is extremely dense and would benefit from being split or moved to an appendix.

The paper's defensive tone—anticipating and addressing potential criticisms inline—suggests it has been through multiple revision cycles. While thoroughness is appreciated, the result is a paper that spends considerable space justifying its assumptions rather than developing its insights.

## 5. Ethical Compliance

**Rating: 4 (Good)**

The paper includes an explicit acknowledgment of AI-assisted ideation (Claude 4.6, Gemini 3 Pro, GPT-5.2) with appropriate qualification that the AI contributions "motivated aspects of the coordinator architecture but [are] not validated here." This is transparent and appropriate. The reference to a methodology paper [dyson_multimodel] provides traceability.

The anonymous authorship ("Project Dyson Research Team") with a note that "individual author names and affiliations will be provided for final publication per IEEE policy" is acceptable for review but must be resolved before publication. The open-source code availability (GitHub, tagged release) supports reproducibility.

One minor concern: the paper references future AI model versions (Claude 4.6, GPT-5.2) that do not exist as of my knowledge cutoff, suggesting either speculative naming or a future publication date. This should be clarified.

## 6. Scope & Referencing

**Rating: 3 (Adequate)**

The paper is appropriate for IEEE T-AES in scope, addressing autonomous spacecraft coordination at scale. The reference list (52 entries) covers the relevant domains: constellation operations, swarm robotics, distributed systems, queueing theory, and AoI. Key works are cited (Kleinrock, Lamport, Ongaro/Raft, Demers gossip, Kaul/Yates AoI).

Several gaps exist. The paper does not cite recent work on distributed satellite autonomy beyond NASA DSA, such as ESA's OPS-SAT experiments or the growing literature on onboard AI for constellation management. The DTN/BPv7 citation is present but the paper does not engage with how DTN store-and-forward mechanisms would interact with the proposed coordination protocol. The CCSDS Proximity-1 citation for guard-time estimation is appropriate, but the paper does not reference the CCSDS Spacecraft Onboard Interface Services (SOIS) standards that would be relevant for intra-cluster communication.

Several references are non-archival (Amazon Kuiper overview, DARPA program pages, DoD fact sheets, NRL magazine article). While understandable for program descriptions, these weaken the scholarly foundation. The self-citation [dyson_multimodel] to a non-peer-reviewed publication on the project's own website is a concern for a T-AES submission.

The paper does not adequately engage with the satellite networking literature on distributed resource management, particularly work on distributed scheduling for LEO mega-constellations (e.g., Leyva-Mayorga et al., IEEE JSAC 2022; Jia et al., IEEE TWC 2021) that addresses similar scaling challenges from a networking perspective.

---

## Major Issues

1. **Circular validation architecture.** The DES and closed-form equations operate at the same abstraction level. The <0.1% agreement confirms arithmetic consistency, not model validity. The paper needs either (a) a packet-level simulation comparison for at least one configuration, or (b) a much more prominent and explicit framing that this is a parametric design tool, not a validated system model. Currently, the framing oscillates between these two interpretations.

2. **Stress-case infeasibility undermines primary metric.** The stress-case $\eta \approx 46\%$ requires 22 cycles for unicast delivery (Eq. 12), making it physically unrealizable in a single cycle. Yet it is used as the primary comparison metric throughout (Tables V, VI, VII; Figs. 6, 7, 8). The paper should either (a) center the analysis on the event-driven profile ($\eta \approx 6\%$) as the primary metric, with stress-case as a boundary, or (b) redefine the stress-case to be schedulable within a single cycle and accept the lower overhead number.

3. **Incomplete topology comparison.** The four topologies compared provide fundamentally different services (Table IX). The centralized model lacks communication-layer overhead; the global-state mesh is an intentional straw man; the sectorized mesh provides only local awareness. Only the hierarchical architecture is fully modeled. The paper should either (a) restrict quantitative comparison to hierarchical vs. sectorized mesh with explicit service-scope normalization, or (b) develop the centralized communication model to enable fair comparison.

4. **Narrow operating regime relevance.** The 1 kbps budget applies to <1% of operational time (RF backup). Table II shows all interesting results vanish at ≥10 kbps. The paper should more clearly articulate why the RF-backup regime merits this depth of analysis—presumably because it is the design-driving worst case for safety-critical functions—and should present at least one complete analysis at 10 kbps to demonstrate the equations' utility in the primary operating regime.

5. **Missing mission requirements coupling.** The design equations produce numbers (AoI P99 = 441 s, GE recovery P95 = 4 cycles, coordinator ingress = 24 kbps) but never connect them to mission requirements. What AoI is acceptable for conjunction screening? What recovery time is tolerable before collision avoidance degrades? Without this coupling, the equations are descriptive but not prescriptive, limiting their value as a "practitioner toolkit."

---

## Minor Issues

1. **Abstract, line 1:** "We assemble" is vague—specify what is assembled from what (standard results into architecture-specific sizing relationships).

2. **Eq. (2):** The M/D/1 waiting time formula $W_q = \rho / [2\mu_s(1-\rho)]$ is the Pollaczek-Khinchine result for deterministic service, but the standard form is $W_q = \rho^2 / [2\lambda(1-\rho)]$. Please verify the form used is consistent with the Kleinrock reference.

3. **Section III-B-2:** "Static cluster membership for the 1-year duration. This is exact for co-planar formations"—this is only exact for identical orbital elements. Even co-planar satellites with different semi-major axes will drift. Clarify the orbital configuration assumed.

4. **Table IV:** The collision avoidance rate footnote (a) says "screening events, not maneuver-triggering" but the message is labeled "collision avoidance msg" (128 B). Clarify whether this is a screening alert or a maneuver command.

5. **Section IV-A, TDMA frame model:** The derived $\gamma = 0.949$ vs. the assumed $\gamma = 0.85$ represents a 12% discrepancy. The justification for retaining 0.85 (FEC, ranging, control channel) is reasonable but should be quantified more precisely rather than listing approximate percentages.

6. **Eq. (12):** The unicast stagger calculation uses $\alpha_{\text{RX}} = 0.918$ (from the ingress analysis) but this value is not explicitly defined before use. Define $\alpha_{\text{RX}}$ in the notation table.

7. **Table VI (AoI results):** The footnote describes the tail-statistic methodology in detail, which is good practice, but the "sampled every 100 s" introduces discretization. At $T_c = 10$ s, sampling every 100 s means only every 10th cycle is captured. Justify this sampling rate or use every-cycle sampling.

8. **Section IV-C:** "Gilbert-Elliott recovery P95 in 4 cycles" — specify that this is conditioned on starting in the bad state. The unconditional P95 would be different.

9. **Fig. 5 caption:** References "DES bars (30 MC replications, $N = 10,000$, $k_c = 100$)" but the figure is not viewable. Ensure the histogram bin width is specified.

10. **Section V-C, Design Equations Summary:** The geometric approximation for inter-cycle recovery P95 uses $p_{\text{eff}}$ defined as a steady-state mixing probability, but this is not the correct initial condition (should be conditioned on bad state). Clarify.

11. **References:** [1] cites an FCC filing and a non-archival personal website in the same entry. Split these or remove the non-archival component.

12. **Acknowledgment:** "Claude 4.6, Gemini 3 Pro, GPT-5.2" — these version numbers do not correspond to any released models. Clarify whether these are internal designations or future projections.

13. **Data Availability:** The GitHub tag `paper-02-v-bf` suggests this is the second paper from the project. If a first paper exists, it should be cited.

---

## Overall Recommendation

**Major Revision**

The paper addresses a legitimate gap in the literature and provides a useful collection of sizing equations for hierarchical coordination in large spacecraft swarms. The analytical work is internally consistent and the Monte Carlo verification is methodologically sound for what it claims to do. However, five major issues prevent acceptance in the current form: (1) the validation is circular (same-level abstraction checking), (2) the primary metric ($\eta \approx 46\%$) corresponds to a physically infeasible single-cycle workload, (3) the topology comparison is incomplete and potentially misleading, (4) the analysis is confined to a narrow operating regime (<1% of operational time), and (5) the design equations are not coupled to mission requirements. A major revision addressing these issues—particularly recentering on the event-driven workload, adding at least a single-cluster packet-level validation, and connecting AoI/recovery metrics to conjunction assessment requirements—would substantially strengthen the contribution.

---

## Constructive Suggestions

1. **Recenter on the event-driven workload.** Make $\eta_E \approx 6\%$ the primary analysis case and relegate the stress case to a boundary check. This eliminates the 22-cycle schedulability issue, makes the results more operationally relevant, and actually strengthens the paper's message: hierarchical coordination adds only ~6% overhead for representative operations.

2. **Add a single-cluster packet-level validation.** An NS-3 or OMNeT++ simulation of one cluster ($k_c = 100$) with TDMA PHY, realistic propagation, and half-duplex constraints would transform the paper from a parametric exercise into a validated design tool. Even a simplified model showing that message-layer predictions hold within 10–15% at the packet level would be sufficient. This is acknowledged as future work (Section V-A) but is essential for T-AES publication.

3. **Develop a mission requirements interface.** Define acceptable AoI thresholds for conjunction screening (e.g., based on Alfano [51] collision probability sensitivity to state age), acceptable recovery times for collision avoidance (e.g., time-to-closest-approach distributions from ESA [47]), and acceptable coordinator outage durations. Then show which regions of the design parameter space satisfy these requirements. This converts the descriptive equations into prescriptive design guidance.

4. **Consolidate the coordinator bandwidth analysis.** Section IV-A presents three models, two command types, TDMA feasibility, synchronization, and guard-time sensitivity in a single subsection. Split this into: (a) primary TDMA sizing result (one page), (b) robustness analysis (synchronization loss, guard-time sensitivity) as a separate subsection. The current presentation buries the key result (24 kbps under TDMA) in extensive secondary analysis.

5. **Normalize the topology comparison by service scope.** Define a "coordination service unit" (e.g., bits per node per cycle per neighbor monitored) and compare topologies on this normalized basis. This would make the hierarchical vs. sectorized mesh comparison fair and quantitative rather than requiring qualitative caveats about functional scope.