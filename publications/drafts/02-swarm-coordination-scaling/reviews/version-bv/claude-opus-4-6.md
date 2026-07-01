---
paper: "02-swarm-coordination-scaling"
version: "bv"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-27"
recommendation: "Major Revision"
---

# Peer Review: "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms"

**Manuscript Version:** BV
**Venue:** IEEE Transactions on Aerospace and Electronic Systems

---

## 1. Significance & Novelty

**Rating: 3 (Adequate)**

The paper addresses a genuine gap: there is no published work providing closed-form parametric sizing equations for coordination architectures spanning $10^3$–$10^5$ autonomous space nodes with byte-level traffic accounting. The three-layer feasibility decomposition (byte budget, MAC efficiency, TDMA airtime) is a useful conceptual framework that practitioners could apply. The identification that architecture-specific overhead ($\eta_0 \approx 5\%$) is small while topology-invariant command traffic dominates the stress case is a clean and potentially impactful finding.

However, the novelty is tempered by the fact that the core analytical results are relatively straightforward traffic accounting exercises. The overhead equation $\eta = \eta_0 + \eta_{\text{cmd}}$ is essentially a summation of known message sizes divided by a fixed bandwidth budget. The AoI result (Eq. 12) is a direct application of geometric waiting times. The GE inter-cycle recovery is a standard Markov chain calculation. While the *combination* and *application context* are new, the individual analytical contributions are modest. The paper would benefit from a clearer articulation of which specific results are non-obvious—for instance, the ARQ infeasibility under per-cycle GE coherence and the 22-cycle unicast stagger requirement are genuinely useful design insights that deserve more prominence relative to the extensive verification machinery.

The claimed scale range ($10^3$–$10^5$) is somewhat misleading given that the DES validates up to $10^5$ but the $O(1)$ scaling of $\eta$ with $N$ means there is essentially nothing *happening* at different scales—the overhead is constant by construction (Eq. 4 with fixed $k_c$). The interesting scaling questions (cluster re-association dynamics, inter-cluster interference, visibility-constrained topology changes) are all deferred to future work.

## 2. Methodological Soundness

**Rating: 3 (Adequate)**

The methodology has a clear and internally consistent structure: closed-form equations are derived, a cycle-aggregated DES confirms implementation consistency, and a slot-level TDMA simulator validates superframe timing. The authors are commendably transparent about what is and is not modeled. The three-layer feasibility framework is well-motivated.

**Strengths:** The paper is unusually honest about its abstraction level. The explicit enumeration of "not modeled" items (Section III-B), the careful distinction between fluid-server DES and TDMA slot scheduling, and the repeated caveats about message-layer vs. physical-layer validity are exemplary. The GE coherence-time sensitivity analysis (Fig. 7) is a valuable addition that contextualizes the ARQ infeasibility claim. The open-source commitment with tagged releases enhances reproducibility.

**Concerns:** The DES is cycle-aggregated with fluid-server ingress, meaning it cannot capture the very phenomena that would stress the design equations: slot-level contention, half-duplex scheduling conflicts, and the interaction between GE losses and TDMA frame timing. The authors acknowledge this (Table VI footnote), but the consequence is that the DES provides almost no independent validation beyond confirming arithmetic. The $<0.1\%$ agreement (Table VIII) is expected when the DES implements the same traffic accounting as the closed-form equations—this is a code verification, not a validation. The slot-level TDMA simulator partially addresses this gap but is limited to a single cluster.

The 30 MC replications with SD $< 0.001\%$ for overhead (Section III-D) raises a question: if the variance is this small, the system is essentially deterministic for overhead calculations, and the MC apparatus adds little beyond confirming the closed-form. The MC is more meaningful for tail statistics (GE recovery, AoI P99), but the paper does not clearly separate these two uses.

The static topology assumption is a significant limitation for LEO constellations. The quantitative bound ($f_h = 0.8\%$, Section V-B) assumes independent re-associations, but in practice, orbital plane crossings create correlated cluster-boundary events affecting many nodes simultaneously. The $<0.5\%$ overhead claim needs more rigorous justification for cross-plane geometries.

## 3. Validity & Logic

**Rating: 3 (Adequate)**

The internal logic is generally sound, and the authors are careful to qualify claims. The decomposition $\eta = \eta_0 + \eta_{\text{cmd}}$ is valid under the stated assumptions. The observation that $\eta_{\text{cmd}}$ is topology-invariant (given centralized command generation) is correct and important.

**Key validity concerns:**

First, the 1 kbps design point drives most of the interesting results but is described as an RF-backup scenario occurring $<1\%$ of operational time (Section III-E). This creates a tension: the paper's primary contributions (coordinator bottleneck, TDMA requirement, ARQ infeasibility, 22-cycle stagger) apply only to a degraded-mode edge case. At the nominal $\geq$10 kbps, "all message-layer constraints are non-binding" (Table I). The paper should more clearly frame whether it is sizing a backup system or a primary coordination architecture.

Second, Table VI (Joint Interaction) shows identical drop counts for "No Loss" and "GE Only" columns, which the authors explain as pipeline decoupling under dedicated links. But this means the DES's GE model has *zero effect* on coordinator queue behavior—the GE losses and queue drops are completely independent mechanisms that never interact. This is an artifact of the fluid-server model, not a physical property of the system. Under actual TDMA, corrupted packets consume slot time (as the authors note), creating the very interaction the DES cannot capture.

Third, the centralized baseline uses an intentionally low $\mu_s = 1{,}000$ msg/s to create a compute bound at $N = 10^4$. With $c = N/k_c$ parallel servers, it scales to $10^6$. This makes the centralized "reference bound" somewhat arbitrary—it can be made to scale to any desired $N$ by increasing $c$. The comparison in Fig. 10 and Table IX is therefore less informative than it appears.

Fourth, the coordinator failure transient analysis (Section III-B.2) identifies RF-backup recovery at ~160 s (16 cycles) as the design-driving case, but the AoI impact is described as "modest vs. P99 = 441 s." This comparison conflates two different phenomena: the 441 s P99 is for exception telemetry under normal operations, while the 160 s transient is a failure recovery scenario. These should not be compared as if they are on the same scale of concern.

## 4. Clarity & Structure

**Rating: 4 (Good)**

The paper is well-organized with a clear roadmap (beginning of Section IV) and consistent notation (Table I). The three-layer feasibility framework provides a useful organizing principle. Tables are generally well-constructed with informative footnotes. The explicit "reading guide" in Table VII footnotes is helpful.

The writing is dense but precise. The authors make good use of inline qualifications ("under the assumed message model," "message-layer predictions") that prevent overclaiming. The Design Equations Summary (Section V-C) is a valuable practitioner-oriented contribution.

**Areas for improvement:** The paper is excessively long for the analytical content it delivers. Much space is devoted to verifying that a DES implementing the same equations as the closed-form produces the same numbers. Sections IV-F through IV-I could be substantially compressed. The sectorized mesh discussion (Section III-B.4, Table IV) is disproportionately detailed for what is acknowledged as a "local-neighborhood baseline, not a coordination architecture comparable to the hierarchy."

The abstract is accurate but very dense—it reads more like a technical summary than an abstract. The sentence "An open-source Monte Carlo tool confirms implementation consistency to $<0.1\%$" could be misread as physical validation rather than code verification.

Figure references are numerous but several figures (Figs. 1, 5, 6, 9–14) are referenced without being viewable in the LaTeX source, making it impossible to assess their quality. The paper would benefit from consolidating some figures into multi-panel displays.

## 5. Ethical Compliance

**Rating: 4 (Good)**

The AI-assistance disclosure in the Acknowledgment section is forthright: "An AI-assisted ideation exercise (Claude 4.6, Gemini 3 Pro, GPT-5.2; see [52]) motivated aspects of the coordinator architecture but is not validated here." This is appropriately transparent. The data availability statement with tagged repository is commendable.

The anonymous authorship ("Project Dyson Research Team") with a note about final publication is acceptable for review but must be resolved before publication per IEEE policy. The reference to future model versions (Claude 4.6, GPT-5.2) suggests the paper may be from a future date or uses speculative version numbers—this should be clarified.

No conflicts of interest are explicitly declared beyond the project affiliation. Given the open-source nature of the work and absence of commercial interests, this appears adequate.

## 6. Scope & Referencing

**Rating: 3 (Adequate)**

The paper is appropriate for IEEE TAES in its treatment of autonomous spacecraft coordination, though it sits at the boundary between systems engineering and communications/networking. The reference list is comprehensive (55 references) and covers the relevant domains: constellation operations, swarm robotics, distributed systems, queueing theory, and AoI.

**Concerns:** Several references are non-archival (Amazon Kuiper overview, DARPA program pages, DoD fact sheets, NRL magazine article). While understandable for operational programs, these weaken the scholarly foundation. The Starlink reference [1] is an FCC filing supplemented by a non-archival personal website—a peer-reviewed source on Starlink operations would strengthen the motivation.

The paper cites LEACH [55] as inspiration for coordinator rotation but does not engage deeply with the extensive WSN clustering literature (HEED, TEEN, PEGASIS, etc.) that has analyzed similar overhead-vs-aggregation tradeoffs. Given that the core contribution is overhead sizing for hierarchical clustering, this literature deserves more thorough treatment.

The AoI framework citations [48–50] are appropriate, but the paper does not engage with the substantial body of work on AoI-optimal scheduling under energy harvesting or TDMA constraints (e.g., work by Modiano's group, Sun/Uysal-Biyikoglu), which is directly relevant to the coordinator scheduling problem.

Missing from the related work: recent papers on distributed space systems autonomy (e.g., the CADRE mission, ESA's OPS-SAT experiments), which provide empirical data points for onboard coordination overhead.

---

## Major Issues

1. **The DES provides code verification, not validation.** The $<0.1\%$ agreement between DES and closed-form (Table VIII) is expected when both implement the same traffic accounting. The paper repeatedly presents this as a key result, but it demonstrates only that the code correctly implements the equations—not that the equations correctly model physical systems. The slot-level TDMA simulator is a step toward validation but covers only a single cluster. The paper should clearly distinguish verification (DES vs. equations) from validation (model vs. reality) and reduce the emphasis on the former. The current framing risks misleading readers into thinking the model has been validated to 0.1% accuracy.

2. **The 1 kbps design point creates a mismatch between the paper's framing and its applicability.** The title and abstract suggest general "design equations for hierarchical coordination," but the interesting results (coordinator bottleneck, TDMA requirement, ARQ infeasibility, unicast stagger) apply only to the RF-backup edge case. At the nominal $\geq$10 kbps, all constraints are non-binding. The paper should either (a) reframe as explicitly sizing the RF-backup degraded mode, or (b) identify design-driving constraints that persist at higher bandwidths (which would require modeling the currently-excluded physical-layer effects).

3. **The fluid-server DES cannot capture TDMA-GE interaction.** Table VI demonstrates that GE losses and coordinator drops are independent in the DES—but the authors themselves note that under TDMA, corrupted packets consume slot time, coupling these mechanisms. This means the joint interaction verification (Section IV-D) validates a property of the *model*, not of the *system*. The paper should explicitly state that the independence result is an artifact of the fluid-server abstraction and that the recommended NS-3 simulation must specifically test this coupling.

4. **Topology comparison is not apples-to-apples.** The centralized baseline models only compute-queue scalability (no communication overhead), the global-state mesh is an intentional worst case, and the sectorized mesh provides different functional scope. While the authors acknowledge these differences (Table X, footnotes), the comparison figures (Fig. 10) and topology comparison table (Table IX) still invite direct comparison. The paper should either provide a fair comparison (all architectures modeled at the same layer) or remove the comparative framing and focus solely on the hierarchical architecture's absolute sizing.

## Minor Issues

1. **Eq. 2 ($W_q$):** The $M/D/1$ waiting time formula is stated without the standard derivation context. For an $M/D/1$ queue, $W_q = \rho/(2\mu_s(1-\rho))$ is the Pollaczek-Khinchine result for deterministic service. The notation $\mu_s$ (messages/s) vs. the standard $\mu$ (service rate) should be clarified.

2. **Table III (Simulation Parameters):** The collision avoidance rate of $10^{-4}$/node/s yields ~0.86 alerts/node/day. The footnote says these are "screening notifications," but the 128 B message size and priority framing suggest operational alerts. Clarify the operational concept.

3. **Section III-B.2, RF-backup handoff:** The calculation "$51 \times 0.8 / 0.36$ s $\approx 113$ s" is unclear. If 51 responders each send 100 B (= 800 bits) at 1 kbps with Slotted ALOHA throughput 0.36: $51 \times 800 / (1000 \times 0.36) = 113.3$ s. This should be written more explicitly.

4. **Eq. 6 ($M_{\text{mesh}}$):** The fanout $f = N/\log N$ is described as "chosen for single-cycle convergence" but this is not standard gossip. Standard epidemic gossip with fanout $f = O(\log N)$ converges in $O(\log N)$ rounds. The choice $f = N/\log N$ is extreme and makes the mesh comparison less meaningful.

5. **Table V (Sector Cap Sweep):** The $\eta > 100\%$ entry for $k_s - 1$ is physically meaningful (demand exceeds capacity) but the table should note this means the configuration is infeasible, not just high-overhead.

6. **Section IV-A, "Fleet-wide TDMA cost is 0.28 kbps/node":** This calculation (1% coordinators × 24 kbps / 100 nodes × some factor) should be shown explicitly.

7. **Acknowledgment:** "Claude 4.6" and "GPT-5.2" appear to be future/speculative model versions. If these are actual tools used, clarify; if speculative, remove specific version numbers.

8. **Reference [1]:** "See also: J. McDowell, 'Jonathan's Space Report'" is informal for IEEE TAES. Either cite it properly or remove.

9. **Table I notation:** $\eta_{\text{total}}$ is defined as $\eta + 20.5\%$ baseline, but the 20.5% is not defined until Section III-E. Forward-reference or reorder.

10. **Eq. 12 (AoI P99):** The ceiling function is applied to $\ln(0.01)/\ln(1-p_{\text{exc}})$, which is correct for discrete geometric waiting, but the equation should note this is the number of *cycles*, multiplied by $T_c$ to get seconds.

---

## Overall Recommendation

**Major Revision**

The paper addresses a legitimate gap in the literature and provides a useful framework for sizing hierarchical coordination in large space swarms. The three-layer feasibility decomposition, the design equations summary, and the honest treatment of limitations are commendable. However, the paper suffers from three fundamental issues that require substantial revision: (1) the DES verification is presented with disproportionate emphasis relative to its actual contribution (confirming arithmetic), while the genuinely useful slot-level TDMA results receive less attention; (2) the design-driving results apply only to a degraded RF-backup mode that the paper does not consistently frame as such; and (3) the topology comparisons are not conducted at equivalent abstraction levels, undermining the comparative claims. A major revision should reframe the contribution around the design equations themselves (which are the lasting value), reduce the verification apparatus, and either provide fair topology comparisons or focus exclusively on hierarchical sizing.

---

## Constructive Suggestions

1. **Restructure around the design equations as the primary contribution.** Move the Design Equations Summary (currently Section V-C) to be the centerpiece of the results, with the DES and TDMA simulator serving as supporting verification. This would reduce the paper length by ~30% while sharpening the contribution. The current structure buries the most useful content (the closed-form equations and their sensitivity) under extensive simulation verification of limited independent value.

2. **Conduct a single-cluster NS-3 (or equivalent packet-level) simulation.** Even a simplified packet-level model of one 100-node cluster with actual TDMA slot scheduling, half-duplex constraints, and GE-correlated losses would provide genuine validation that the current DES cannot. This would directly address Major Issue #3 and transform the paper from "message-layer predictions pending validation" to "validated at the single-cluster level with fleet-level extrapolation." The authors already identify this as the priority next step—doing it before publication would substantially strengthen the paper.

3. **Explicitly frame the 1 kbps results as RF-backup degraded-mode sizing.** Add a subsection or prominent discussion paragraph explaining that the primary operational mode uses optical ISLs at $\geq$10 kbps where all constraints are non-binding, and that the 1 kbps analysis sizes the backup system that must sustain coordination during ISL outages. This reframing would make the contribution more honest and arguably more valuable—sizing degraded-mode backup systems is a real engineering need.

4. **Replace the four-topology comparison with a focused hierarchical-only analysis plus one fair comparator.** Drop the centralized and global-state mesh baselines (which are not modeled at the same layer) and focus the comparison on hierarchical vs. sectorized mesh, which are both fully modeled. Alternatively, model the centralized architecture at the communication layer (including uplink scheduling and ground contact constraints) to enable a fair comparison. The current asymmetric comparison weakens rather than strengthens the paper.

5. **Expand the GE parameter sensitivity into a practitioner-oriented design chart.** Figure 8(b) is one of the most useful results in the paper. Expand it into a two-dimensional design chart (axes: $p_{BG}$ and $p_B$; contours: P95 recovery cycles and required buffer size) with annotations mapping to physical obstruction mechanisms (structural shadowing, antenna mispointing, etc.). This would make the paper directly usable by mission designers, which is the stated goal.