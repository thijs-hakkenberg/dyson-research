---
paper: "02-swarm-coordination-scaling"
version: "bc"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-27"
recommendation: "Major Revision"
---

# Peer Review: "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms"

## 1. Significance & Novelty
**Rating: 3 (Adequate)**

The paper addresses a genuine gap: there is no consolidated reference for closed-form sizing relationships for hierarchical coordination architectures at the $10^3$–$10^5$ node scale with byte-level traffic accounting. The "practitioner toolkit" framing is appealing, and the identification that architecture-specific overhead (~5%) is dwarfed by topology-invariant command traffic (>60%) is a useful insight that could influence system-level trade studies.

However, the novelty is limited in a fundamental sense. The authors candidly state they "assemble standard queueing, geometric, and Markov-chain results" — the individual analytical components (M/D/1 queueing, geometric AoI distributions, Gilbert-Elliott channel models, gossip convergence bounds) are textbook material. The contribution is therefore one of *integration and application* rather than methodological advance. For IEEE T-AES, this could still be valuable if the application context were sufficiently compelling, but the paper operates entirely at the message layer with no physical-layer validation, no orbital dynamics, and no real channel measurements. The operating regime (1 kbps RF backup, <1% of operational time) is acknowledged as an edge case, which further narrows the practical impact. The claim of applicability to $10^5$ nodes is validated only by a cycle-aggregated DES that, by construction, must agree with the closed forms it implements — this is arithmetic verification, not independent validation.

The paper would be significantly more impactful if it demonstrated that the sizing equations produce non-obvious design insights or if the equations were validated against a higher-fidelity simulation or operational data. As written, the primary finding — that commands dominate overhead and architecture-specific costs are small — could arguably be anticipated from a back-of-envelope calculation once the message model is specified.

## 2. Methodological Soundness
**Rating: 3 (Adequate)**

The analytical framework is internally consistent and clearly specified. The byte-level traffic accounting (Tables IV, V, VI) is thorough, the GE channel model is properly formulated with explicit coherence assumptions, and the Markov recovery derivation (Section IV-C) is correct. The TDMA frame analysis (Eqs. 7–12) is well-structured, and the half-duplex partitioning analysis is a welcome addition that many papers omit.

The central methodological concern is the **circularity of the DES validation**. The DES and the closed-form equations operate at the same abstraction level with the same message model. The <0.1% agreement (Table VIII) confirms only that both computations implement the same arithmetic — it does not validate the model against reality. The authors acknowledge this explicitly (Section III-A: "their agreement confirms arithmetic consistency, not physical fidelity"), which is commendable, but this means the paper's empirical contribution reduces to the inter-cycle GE recovery tail statistics (Fig. 6), which are themselves derivable from the Markov chain (and shown to match). The DES therefore adds very little independent information.

Several specific methodological concerns:

- **The $\sqrt{N}$ sector sizing** (Section III-B.4) is described as "an order-of-magnitude heuristic" without derivation or citation. The claim that "a conjunction screening volume contains $O(\sqrt{N})$ nodes when the screening radius scales with mean nearest-neighbor distance" needs justification — the scaling depends on the dimensionality of the spatial distribution and the screening volume geometry.

- **The collision avoidance rate** ($10^{-4}$/node/s) is stated as "screening events, not maneuvers" but the sensitivity analysis ($\pm 1.5$ pp) suggests this parameter barely matters. If so, why include it? If it does matter operationally, the rate should be better justified for the target constellation geometries.

- **Static cluster membership** is a significant simplification for LEO mega-constellations. The analytical bound on re-association overhead (<0.5%) in Section V-C is reasonable for byte overhead but does not address the coordination disruption during handoff (acknowledged but not quantified beyond "1–3 cycles").

- **The Monte Carlo configuration** (30 replications) is adequate for mean estimation but may be insufficient for the tail statistics (P99 AoI, P95 recovery) that are central claims. The per-run-then-aggregate methodology (Table V footnote) is appropriate, but the paper should report bootstrap CIs for all tail metrics, not just AoI.

## 3. Validity & Logic
**Rating: 3 (Adequate)**

The logical structure is generally sound, and the authors are commendably transparent about limitations. The separation of $\eta$ (protocol overhead beyond baseline) from $\eta_{\text{total}}$ (including baseline telemetry) is clearly maintained throughout. The pipeline decoupling result (Section IV-D, Table VII) — that GE losses and coordinator queue drops are independent under dedicated links — is correctly derived and practically useful, with the important caveat about shared-medium access properly noted.

Several validity concerns:

1. **Functional inequivalence of compared architectures.** The paper compares byte-level overhead across architectures that provide fundamentally different services. The hierarchical architecture provides "full cluster awareness" (100 members), while the capped sectorized mesh provides "3.2% local awareness" (10 neighbors). The authors acknowledge this (Section III-B.4: "These architectures serve different operational needs"), but then proceed to make overhead comparisons (e.g., "sectorized mesh maintains a 1.4–1.5× overhead ratio") that implicitly suggest the hierarchical architecture is more efficient. A fair comparison would normalize by the *information delivered* (bits of useful state awareness per bit of overhead), not just total bytes. This is a significant logical gap.

2. **The "stress-case" dominance of commands.** The finding that commands dominate overhead (>60%) and are topology-invariant is presented as a key insight, but it follows directly from the message model: if you define a stress case where every node receives a 512-byte command every cycle, and the baseline protocol traffic is ~50 bytes/cycle, then of course commands dominate. This is a property of the *assumed workload*, not a discovered property of the architecture.

3. **Extrapolation beyond validated range.** Fig. 8 includes a $10^6$-node curve labeled as "analytical extrapolation, not DES-measured." While this is properly caveated, the $O(N)$ scaling that justifies the extrapolation assumes the hierarchical structure remains valid at $10^6$ — but coordinator-of-coordinator bottlenecks, inter-regional routing complexity, and topology dynamics at that scale are not analyzed.

4. **The centralized baseline is too weak.** Setting $\mu_s = 1{,}000$ msg/s for a single server creates an artificial bottleneck at $N = 10^4$. Modern ground systems process orders of magnitude more. The $M/D/c$ extension ($c = N/k_c$) is more realistic but is not modeled at the communication layer, making the comparison asymmetric (acknowledged in Table IX footnote d, but this undermines the comparative claims).

## 4. Clarity & Structure
**Rating: 4 (Good)**

The paper is well-organized with a clear roadmap (Section IV opening paragraph) and consistent notation (Table I). The separation of contributions into architecture-specific overhead, workload-dependent overhead, coordinator sizing, and correlated loss recovery provides a logical progression. Tables are generally well-formatted and informative, particularly the traffic accounting tables (IV, V, VI) and the bandwidth scaling summary (Table II).

The writing is precise but occasionally over-hedged, with extensive inline caveats that interrupt the flow. For example, the command dissemination model discussion (Section IV-A, around Eqs. 10–11) includes Type 1/Type 2 distinctions, PHY egress calculations, and TDMA feasibility constraints that could be consolidated into a single coherent subsection rather than interspersed with the coordinator capacity analysis.

The paper is quite long for the depth of new results. Much of the length comes from exhaustive specification of what is *not* modeled (Table III), sensitivity analyses that confirm expected linear relationships, and repeated restatements of the same caveats. The Design Equations Summary (Section V-D) is valuable but partially redundant with the results sections.

Specific clarity issues:
- The notation $\eta$ vs. $\eta_{\text{total}}$ vs. $\eta_{\text{eff}}$ vs. $\eta_{\text{delivered}}$ vs. $\eta_{\text{sector}}$ proliferates and becomes difficult to track. A consolidated notation table for all overhead variants would help.
- Fig. 1 is referenced but described only in the caption; the architecture diagram deserves more textual explanation of the information flows.
- The abstract packs too many numbers (26%, 46%, 21–25 kbps, 440 s, 4 cycles, <0.1%) without sufficient context for a reader encountering the paper for the first time.

## 5. Ethical Compliance
**Rating: 4 (Good)**

The AI-assistance disclosure in the Acknowledgment section is transparent: "An AI-assisted ideation exercise (Claude 4.6, Gemini 3 Pro, GPT-5.2; see [52]) motivated aspects of the coordinator architecture but is not validated here." This is appropriately scoped and honest. The open-source data availability statement with a specific repository tag is commendable and supports reproducibility.

The anonymous authorship ("Project Dyson Research Team" with a footnote promising individual names for final publication) is unusual but not necessarily problematic for review purposes. The IEEE policy reference is appropriate.

One minor concern: the reference to future AI model versions (Claude 4.6, GPT-5.2) that do not exist as of mid-2025 suggests either a speculative timeline or a fictional framing. This should be clarified — if these are placeholder names, they should be replaced with actual tool versions used.

## 6. Scope & Referencing
**Rating: 3 (Adequate)**

The paper is broadly appropriate for IEEE T-AES, which publishes work on space systems, autonomous operations, and communication architectures. However, the absence of any physical-layer content (no link budgets, no orbital geometry, no actual constellation parameters) places it closer to a communications/networking venue (e.g., IEEE JSAC, IEEE TWC) or a systems engineering journal.

The reference list is comprehensive (55 references) and covers the relevant domains: constellation operations, swarm robotics, distributed systems, queueing theory, and AoI. Key omissions include:

- **Recent mega-constellation coordination work**: The paper does not cite Portillo et al.'s more recent work on constellation design optimization, or the growing literature on autonomous collision avoidance (e.g., Merz et al., ESA's CREAM system).
- **DTN/contact-graph routing**: Beyond the BPv7 citation, the paper does not engage with the substantial literature on contact-graph routing for LEO constellations, which is directly relevant to the intermittent-link regime.
- **Space-qualified radio specifications**: The claim that "21–25 kbps coordinator ingress is within the capability of modest space-qualified transceivers" (citing only SMAD) would benefit from specific radio references (e.g., Cadet, Iris, or similar S-band radios with published specifications).
- **Several references are non-archival** (Amazon Kuiper overview, DARPA program pages, DoD fact sheets). While understandable for program descriptions, these weaken the scholarly foundation.

---

## Major Issues

1. **The DES provides no independent validation.** The <0.1% agreement between DES and closed-form equations is presented as a key result, but since both implement the same message-layer model, this is tautological. The paper needs either (a) a higher-fidelity simulation (packet-level, NS-3/OMNeT++) to quantify the message-to-packet gap, or (b) a much more explicit framing that this is a *design equation reference*, not an empirical study. Currently, the paper occupies an uncomfortable middle ground.

2. **Functional inequivalence undermines topology comparisons.** Comparing byte-level overhead between architectures that deliver fundamentally different levels of state awareness (100% cluster vs. 3.2% local) is misleading. The paper needs either (a) a normalized efficiency metric (bits of awareness per bit of overhead), or (b) a clear statement that cross-topology overhead comparisons are not meaningful and should be removed from the narrative.

3. **The 1 kbps operating regime is too narrow for the claimed generality.** Table II shows that at ≥10 kbps, the coordinator bottleneck and TDMA requirement vanish, and the remaining equations (AoI, GE recovery) are bandwidth-independent. This means the most interesting results (coordinator sizing, TDMA analysis) apply only to the RF-backup edge case (<1% of operational time). The paper should either (a) provide substantive analysis at 10–100 kbps where different bottlenecks emerge, or (b) retitle/reframe as specifically addressing the RF-backup degraded mode.

4. **Tail statistics need stronger statistical treatment.** The P99 AoI (441 s) and P95 GE recovery (4 cycles) are central claims but are reported from only 30 MC replications. For extreme quantiles, the effective sample size for P99 estimation from 30 runs is very small. The paper should report bootstrap confidence intervals for all tail metrics and discuss the statistical power of the tail estimates.

5. **The stress-case workload assumption drives the headline result but is not justified operationally.** One 512-byte unique command per node per cycle (every 10 seconds, to all 100,000 nodes) is an extreme assumption. What operational scenario requires individualized commands to every satellite every 10 seconds? Station-keeping maneuvers occur on timescales of days to weeks; conjunction avoidance affects <1% of nodes at any time. The event-driven profile ($\eta_E \approx 6\%$) is far more realistic and should be the primary reported result.

## Minor Issues

1. **Eq. 2 (M/D/1 waiting time):** The standard Pollaczek-Khinchine formula for M/D/1 is $W_q = \rho/(2\mu_s(1-\rho))$, which is correct, but the notation conflates service rate $\mu_s$ (messages/s) with the deterministic service time $1/\mu_s$. Clarify units.

2. **Table I:** $\eta$ is defined as "Protocol overhead fraction (beyond baseline)" but $\eta_{\text{total}}$ is defined as "$= \eta + 20.5\%$ baseline." The 20.5% should be derived or cross-referenced earlier (it appears to come from $256 \times 8 / (1000 \times 10) = 20.48\%$, but this is not stated until Section III-E).

3. **Section III-B.2:** "Each cluster coordinator sends a single 512-byte summary per cycle (vs. forwarding $k_c$ individual reports)" — the compression ratio ($k_c \times 256$ B → 512 B) implies significant information loss. What is the summary content? Mean orbital elements plus covariance (Table IV) at 512 B seems tight for 100 satellites.

4. **Eq. 6 ($\gamma$ derivation):** The guard time calculation assumes 500 km cluster diameter, but this is not justified for any specific constellation geometry. At 550 km altitude, a 500 km cluster spans ~5° of arc — is this consistent with $k_c = 100$ in a Walker constellation?

5. **Table VII (Joint interaction):** The "GE + Exc." column shows dramatically fewer drops than "No Loss" at the same $C_{\text{coord}}$. This is because exception telemetry reduces offered load, not because of any GE interaction. The column header is misleading — it should be labeled "Exc. only" or "Exc. + GE" with a note that the reduction is from load shedding.

6. **Section IV-A, TDMA synchronization:** The fallback to Slotted ALOHA upon sync-beacon loss is described but the transition dynamics (how many cycles of degraded performance, probability of false alarm on "two consecutive misses") are not analyzed.

7. **Acknowledgment:** "Claude 4.6, Gemini 3 Pro, GPT-5.2" — these version numbers do not correspond to any released models as of mid-2025. Clarify whether these are actual tools used or speculative references.

8. **Fig. 8 caption:** "the $10^6$-node curve is an analytical extrapolation" — this should be a dashed or dotted line in the figure, not a solid line, to visually distinguish it from validated results.

9. **Section III-B.3:** The gossip redundancy factor "~1.4×" is stated without derivation. Standard epidemic gossip has redundancy $\sim e \ln N / N$ per entry; at $N = 10^5$ this is much less than 1.4×. Clarify the source of this factor.

10. **Throughout:** The paper uses "favorable" (e.g., "$k_c = 100$–200 is favorable") where "recommended" or "preferred" would be more precise. "Favorable" implies a comparison that is not always explicit.

## Overall Recommendation

**Major Revision**

The paper addresses a legitimate gap in providing consolidated sizing relationships for hierarchical space swarm coordination, and the analytical framework is internally consistent. However, the contribution is undermined by three fundamental issues: (1) the DES validation is circular by construction, providing no independent confirmation of model fidelity; (2) the topology comparisons are between functionally inequivalent architectures, making overhead comparisons misleading; and (3) the most interesting results (coordinator sizing, TDMA analysis) apply only to a narrow edge case (<1% of operational time at 1 kbps). The paper would benefit substantially from either a packet-level validation study or a reframing as a pure design-equation reference with the comparative claims removed. The stress-case workload assumption needs operational justification, and the statistical treatment of tail metrics needs strengthening.

## Constructive Suggestions

1. **Add a single-cluster packet-level simulation** (NS-3 or OMNeT++, $k_c = 100$, TDMA PHY) to quantify the message-to-packet overhead gap. This is identified as future work but would transform the paper from an arithmetic exercise into an empirically grounded contribution. Even a simplified PHY model would suffice.

2. **Define a normalized efficiency metric** such as "bits of state awareness delivered per bit of protocol overhead" and use it for cross-topology comparisons. This would make the hierarchical vs. sectorized mesh comparison meaningful and could reveal that the hierarchical architecture is dramatically more *efficient* (not just lower overhead) — which would be a stronger result than the current byte-level comparison.

3. **Promote the event-driven workload ($\eta_E \approx 6\%$) as the primary result** and relegate the stress-case to a sensitivity bound. This better represents operational reality and makes the ~5% architecture-specific overhead finding more prominent and impactful. The current framing buries the most interesting finding (architecture costs are negligible) behind a less interesting one (commands dominate when you assume lots of commands).

4. **Extend the analysis to the 10–100 kbps regime with new bottleneck identification.** Table II shows that coordinator capacity and TDMA requirements vanish at ≥10 kbps, but does not identify what *does* become the binding constraint. Is it AoI? Coordinator processing? Regional aggregation? Identifying the bottleneck transition as a function of bandwidth would significantly increase the paper's practical value.

5. **Provide explicit constellation geometry parameters** (altitude, inclination, number of planes, satellites per plane) for at least one reference constellation (e.g., Starlink shell 1: 550 km, 53°, 72 planes × 22 sats) and verify that the assumed cluster diameter (500 km), sector size ($\sqrt{N}$), and re-association frequency are consistent with the orbital mechanics. This would ground the abstract message model in physical reality without requiring full orbital simulation.