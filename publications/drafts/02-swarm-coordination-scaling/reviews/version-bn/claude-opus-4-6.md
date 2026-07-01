---
paper: "02-swarm-coordination-scaling"
version: "bn"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-27"
recommendation: "Major Revision"
---

# Peer Review: "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms"

**Manuscript Version:** BN
**Venue:** IEEE Transactions on Aerospace and Electronic Systems

---

## 1. Significance & Novelty

**Rating: 3 (Adequate)**

The paper addresses a genuine gap: the absence of closed-form parametric sizing equations for hierarchical coordination architectures at the $10^3$–$10^5$ node scale with byte-level traffic accounting. The authors correctly identify that swarm robotics literature operates at 10–100 agents, constellation management addresses ~$10^4$ nodes without byte-level budgets, and networking literature focuses on routing rather than coordination overhead. The three-layer feasibility framework (byte budget, MAC efficiency, TDMA airtime) is a useful conceptual contribution that practitioners could adopt.

However, the novelty is more incremental than the framing suggests. The core analytical results—that per-node overhead is $O(1)$ in a hierarchical architecture with fixed cluster size, that command traffic dominates over topology-specific overhead, and that a coordinator needs ~24 kbps ingress for 100 members at 256 B/cycle—follow relatively directly from the message model assumptions. The $\eta_0 \approx 5\%$ result is essentially a ratio of heartbeat size to budget ($64 \times 8 / 10{,}000 = 5.12\%$); the "design equation" is arithmetic, not a non-obvious scaling law. The GE inter-cycle recovery analysis (Section IV-C) and the AoI characterization under exception telemetry (Section IV-B) provide more substantive analytical contributions, but these are standard applications of Markov chain analysis and geometric distribution tail bounds, respectively.

The claim "to our knowledge, no prior work provides closed-form parametric sizing relationships for coordination architectures across $10^3$–$10^5$ nodes" (Section I-A) is difficult to verify and somewhat overstated. The LEACH literature (cited as [heinzelman_leach]) does provide cluster-head overhead analysis with byte-level accounting, albeit for sensor networks. The distinction that space ISLs have "long propagation, half-duplex, GE fading" is valid but the analytical framework does not deeply exploit these physical differences—the GE model is applied generically, and propagation delay contributes negligibly to the results (Table VII: 1.7 ms out of ~260 ms total latency).

## 2. Methodological Soundness

**Rating: 3 (Adequate)**

The methodology has a clear structure: derive closed-form equations, implement a cycle-aggregated DES, and verify consistency. The three-layer feasibility framework is well-conceived. The explicit TDMA superframe budget (Table V) and the half-duplex TX/RX partitioning analysis are commendable engineering contributions. The separation of architecture-specific overhead ($\eta_0$) from workload-dependent command traffic ($\eta_{\text{cmd}}$) is a useful decomposition.

However, several methodological concerns arise:

**The DES validates the equations but not the model.** The authors acknowledge this (Section V-A: "confirms implementation correctness, not physical validity"), but the paper's structure—with extensive DES results, 30 MC replications, bootstrap CIs—creates an impression of empirical validation that is not warranted. The DES and the closed-form equations share identical assumptions; the $<0.1\%$ agreement (Table VIII) is expected by construction (both compute the same byte sums). The DES adds value only for tail statistics (GE recovery CDF, Fig. 5) where the Markov chain provides the analytical baseline anyway. The 30 MC replications with SD $< 0.001\%$ for overhead are unnecessary for a deterministic quantity—overhead at fixed parameters is not stochastic (it depends only on message counts and sizes, which are deterministic given the workload profile). The stochasticity enters only through GE state transitions and failure events, which affect delivery rates, not offered overhead.

**The fluid-server DES does not enforce TDMA scheduling.** This is acknowledged in Section IV-D ("TDMA slot scheduling and half-duplex partitioning are *not* enforced in the DES"), but it means the joint interaction results (Table VI) are incomplete. The paper's most operationally relevant constraint—the 623 ms superframe margin (Table V)—is never tested in simulation. The claim that "GE recovery and coordinator capacity equations apply independently" (Section IV-D) is validated only under fluid-server assumptions, not under the TDMA frame where corrupted packets consume slot time (as the authors note: "the TDMA frame schedule is *not* decoupled from loss").

**The 1 kbps design point is simultaneously the most interesting and least realistic case.** The paper acknowledges this is an RF-backup scenario ($<1\%$ of operational time), yet devotes the majority of analysis to it. The $\geq$10 kbps regime where "all constraints are non-binding" (Table I) is dismissed in a few sentences. This creates an odd emphasis: the paper's most detailed results apply to a degraded-mode edge case, while the nominal operating regime is trivially unconstrained.

**Statistical methodology for tail statistics needs clarification.** The P99 AoI is reported as "mean of 30 per-run P99 values with 95% bootstrap CI" (Table IV footnote). This is the mean of order statistics, not the fleet-wide P99. With ~$3.15 \times 10^6$ samples per run, the per-run P99 is well-estimated, but the inter-run variability of P99 depends on the tail shape. The bootstrap CI of [438, 444] s is suspiciously tight for a P99 statistic; the authors should clarify whether this reflects the geometric distribution's deterministic quantile (which it essentially is: $\lceil \ln(0.01)/\ln(0.9) \rceil \times 10 = 440$ s exactly).

## 3. Validity & Logic

**Rating: 3 (Adequate)**

The analytical results are internally consistent and the derivations are correct. The AoI P99 formula (Eq. 11) is exact for geometric inter-report intervals. The GE Markov recovery derivation (Section IV-C) is standard and correctly applied. The TDMA capacity equation (Eq. 7) is straightforward dimensional analysis. The superframe budget (Table V) is a useful and correctly computed artifact.

Several logical concerns merit attention:

**The topology comparison is asymmetric and potentially misleading.** The centralized baseline models only compute-queue scalability (M/D/c), not communication overhead. The global-state mesh is an intentional worst case with $O(N^2)$ traffic. The sectorized mesh provides fundamentally different functionality (local monitoring vs. cluster coordination). The authors acknowledge all of this (Table X, footnotes), but the comparison still appears in Fig. 8 and Table IX as if these are peer architectures. The "14× bandwidth efficiency per unit of awareness" claim (Section IV-G) compares hierarchical monitoring of 100 cluster peers against mesh monitoring of 10 local neighbors—but these serve different operational purposes (fleet coordination vs. collision avoidance). A fairer comparison would hold functional scope constant.

**The coordinator failure analysis mixes optimistic and pessimistic assumptions.** The optical-ISL handoff (3–5 s) assumes Gbps rates and successful Raft election. The RF-backup handoff (~160 s) assumes 1 kbps with Slotted ALOHA. The triple-fault probability ($1.8 \times 10^{-5}$/yr) assumes independence of coordinator failure, optical outage, and GE bad-state—but the paper itself notes these "may be correlated if the failure mode is power-negative or tumbling." The stated probability is therefore a lower bound, not a design value.

**The static topology assumption deserves more scrutiny.** The paper bounds re-association overhead at $<0.5\%$ (Section V-B), but this assumes seed handoff only (2 kB). In practice, a new coordinator must rebuild state from incoming reports over 1–3 cycles, during which cluster coordination quality is degraded. For cross-plane LEO configurations with ~45–90 min re-association periods, this means ~0.8% of nodes are in a degraded state at any time—a non-trivial fraction when multiplied by the fleet size ($\sim$800 nodes at $N = 10^5$).

**The command traffic model drives the headline result but is weakly justified.** The stress-case assumes every node receives a 512 B command every cycle ($p_{\text{cmd}} = 1.0$). This is described as an "information-demand upper bound" but no operational scenario is provided where every node in a 100,000-node fleet receives a unique command every 10 seconds. The event-driven profile ($p_{\text{cmd}} = 0.01$, $\eta_E \approx 6\%$) is more realistic but receives less attention. The paper's central finding—that command traffic dominates—is tautological if the stress-case command rate is set arbitrarily high.

## 4. Clarity & Structure

**Rating: 4 (Good)**

The paper is generally well-written and well-organized. The roadmap at the beginning of Section IV is helpful. The notation table (Table I) is clear. The three-layer feasibility framework provides a useful organizing principle. The explicit superframe budget (Table V) is an exemplary engineering artifact. The design equations summary (Section V-C) is a valuable practitioner reference.

Several clarity issues exist:

The paper is dense—arguably too dense for a journal article. The extensive footnotes, parenthetical qualifications, and cross-references (e.g., "see Section~\ref{sec:validation_gap}", "Table~\ref{tab:superframe}", "Eq.~\ref{eq:unicast_stagger}") make linear reading difficult. Many results are stated multiple times with slight variations (e.g., $\eta_0 \approx 5\%$ appears in the abstract, Section I-C items 1–2, Section III-F, Section IV-E, Section V-C, and Section VI). While some repetition aids comprehension, this level suggests the paper could be tightened.

The distinction between $\eta$, $\eta_0$, $\eta_{\text{cmd}}$, $\eta_{\text{total}}$, and $\eta_{\text{eff}}$ is confusing despite the notation table. The notation $\eta_{\text{total}} = \eta + 20.5\%$ means $\eta$ excludes baseline telemetry, but some tables report $\eta_{\text{total}}$ and others report $\eta$, requiring the reader to mentally convert. A single consistent metric throughout would improve readability.

Figures are referenced but not provided (this is a LaTeX source review), so their effectiveness cannot be assessed. The figure captions are generally informative. The number of figures (12+) and tables (12+) is high for a journal paper; some consolidation would be beneficial.

The Acknowledgment section's reference to "Claude 4.6, Gemini 3 Pro, GPT-5.2" with a citation to a Project Dyson publication raises questions about the timeline and version numbers of these AI systems, which do not correspond to any publicly released versions as of mid-2025.

## 5. Ethical Compliance

**Rating: 4 (Good)**

The paper includes an explicit AI-assistance disclosure in the Acknowledgment section, which is commendable and consistent with IEEE policy. The disclosure is appropriately scoped: "motivated aspects of the coordinator architecture but is not validated here." The data availability statement with a specific GitHub tag and reproducibility information is excellent practice.

The anonymous authorship ("Project Dyson Research Team") with a note that "Individual author names and affiliations will be provided for final publication per IEEE policy" is acceptable for review but must be resolved before publication. IEEE requires named authors who can certify originality and take responsibility for the work.

The AI model version numbers cited (Claude 4.6, Gemini 3 Pro, GPT-5.2) do not correspond to publicly known releases, which is puzzling. If these are internal/beta versions, this should be clarified. If they are speculative/future versions, this raises concerns about the paper's provenance.

## 6. Scope & Referencing

**Rating: 3 (Adequate)**

The paper is within scope for IEEE TAES, which publishes work on space systems, autonomous operations, and communication architectures. The combination of coordination architecture design, queueing analysis, and parametric sizing is appropriate for the journal's readership.

The reference list (48 items) is comprehensive and covers the relevant literature: constellation operations (Starlink, Kuiper, OneWeb), swarm robotics (Brambilla, Dorigo), distributed systems (Lamport, Raft), AoI theory (Kaul, Yates, Kadota), queueing theory (Kleinrock), and CCSDS standards. The inclusion of LEACH, SWIM, and Contact Graph Routing demonstrates awareness of adjacent fields.

However, several gaps exist. The paper does not cite recent work on distributed satellite autonomy beyond NASA DSA—e.g., ESA's OPS-SAT experiments, or the growing literature on onboard AI for constellation management. The DTN/CGR literature is cited but not engaged with substantively; the paper's TDMA model could benefit from comparison with CGR's scheduled-access framework. The GE channel model literature for LEO ISLs is thin—the paper cites no empirical characterization of ISL channel statistics, relying instead on generic GE parameters. Some references are non-archival (Amazon Kuiper overview, DARPA program pages, DoD fact sheets); while understandable for program descriptions, these weaken the scholarly foundation. The self-citation [dyson_multimodel] to a Project Dyson publication that appears to be unpublished or non-peer-reviewed is concerning.

---

## Major Issues

1. **The DES provides negligible independent validation.** The $<0.1\%$ agreement between DES and closed-form equations is expected by construction—both compute identical byte sums under identical assumptions. The paper should either (a) implement a packet-level simulation that tests assumptions the closed-form equations cannot capture (MAC contention, half-duplex scheduling, slot-level GE), or (b) substantially reduce the DES presentation and reframe the paper as purely analytical. Currently, the extensive MC apparatus (30 replications, bootstrap CIs, runtime benchmarks) creates a misleading impression of empirical validation. The DES's only independent contribution—GE inter-cycle recovery tail statistics—could be presented more concisely.

2. **The TDMA superframe feasibility is never simulated.** The paper's most operationally critical result—the 623 ms margin in a 10 s cycle (Table V)—is purely analytical. The DES uses fluid-server ingress, not slot-scheduled ingress. The joint interaction results (Table VI) explicitly note that "TDMA slot scheduling and half-duplex partitioning are *not* enforced in the DES." This means the paper cannot validate its own claim that GE losses and coordinator queuing are independent under TDMA (where corrupted packets consume slot time). This is acknowledged as future work, but it undermines the paper's central sizing equations. At minimum, a slot-level analytical model (not just fluid-server) should be developed to bound the interaction.

3. **The stress-case command workload is not operationally motivated.** The headline result ($\eta_S \approx 46\%$) is driven by the assumption that every node receives a 512 B command every 10 s cycle. No operational scenario justifying this rate is provided. The event-driven profile ($\eta_E \approx 6\%$) is more realistic but receives secondary treatment. The paper should either (a) provide concrete operational scenarios that justify the stress-case rate, or (b) reframe the stress-case as a parametric bound and lead with the event-driven profile as the primary result.

4. **The topology comparison lacks a fair baseline.** The centralized model captures only compute-queue scalability (no communication overhead). The global-state mesh is an intentional worst case. The sectorized mesh provides different functionality. No architecture is compared at equivalent functional scope. The paper should either (a) implement a centralized communication model (including uplink scheduling and ground contact constraints) for fair comparison, or (b) remove the cross-architecture comparison and present the hierarchical results standalone with the sectorized mesh as a local-awareness alternative (not a competitor).

5. **GE model parameters lack empirical grounding for LEO ISLs.** The GE parameters ($p_G = 0.01$, $p_B = 0.90$, $p_{GB} = 0.05$, $p_{BG} = 0.50$) are stated without reference to measured LEO ISL channel statistics. The sensitivity sweep (Fig. 5b) partially addresses this, but the default parameters—which drive the headline P95 = 4 cycles result—are not justified against any physical measurement or link budget analysis. The "physical mapping" paragraph (Section IV-C) identifies three obstruction mechanisms but does not map them to specific GE parameter ranges.

---

## Minor Issues

1. **Eq. (2), M/D/1 waiting time:** The formula $W_q = \rho / (2\mu_s(1-\rho))$ is the Pollaczek-Khinchine result for M/D/1, but the notation is slightly non-standard. Clarify that this is the mean waiting time (excluding service) for the M/D/1 queue specifically.

2. **Section III-B.2, Eq. (4):** The message count $M_{\text{total}} = N + N/k_c + N/(k_c \cdot k_r)$ counts upward messages only. Downward commands and heartbeats are mentioned in the text but not in the equation. Consider a complete bidirectional message count equation.

3. **Table II, collision avoidance rate:** $10^{-4}$/node/s is stated as "screening notifications" (footnote a), but the simulation models these as 128 B priority alerts. Clarify whether these trigger autonomous maneuvers or ground-in-the-loop responses, as this affects the command traffic model.

4. **Section IV-A, Model A Monte Carlo:** "Monte Carlo estimate from $10^5$ random arrival patterns" for the $C_A \approx 50$ kbps result is insufficiently documented. What is the confidence interval? What distribution was assumed for arrival times?

5. **Table IV, $p_{\text{exc}} = 1.0$ row:** The $\eta = 46.0\%$ includes "stress-case commands + heartbeats + summaries" per the footnote, but the column header says "Exception telemetry ($p_{\text{link}} = 1.0$, no link loss)." This conflates exception reporting probability with workload profile. Clarify which workload profile each row uses.

6. **Section III-B.4, Eq. (5):** The sector overhead formula uses $\min(k_s - 1, 10) \times 32$ bytes for heartbeats, but the text says "up to $\min(k_s - 1, 10)$ neighbors." Clarify whether the cap of 10 is a design choice or a model limitation.

7. **Table V footnote:** "Under degraded $\gamma = 0.80$: slot duration grows to 98.0 ms, ingress to 9,702 ms, margin shrinks to 98 ms." This 98 ms margin is dangerously thin for a 10 s cycle. The paper should explicitly flag this as a design risk, not just a footnote.

8. **Section V-B, re-association overhead:** The $<0.5\%$ bound assumes seed handoff only (2 kB). State the full overhead including the 1–3 cycle state rebuild period.

9. **Acknowledgment:** "Claude 4.6, Gemini 3 Pro, GPT-5.2" — these version numbers do not correspond to any publicly released AI models. Clarify or correct.

10. **Reference [dyson_multimodel]:** Self-citation to an apparently unpublished Project Dyson document. If not peer-reviewed, label as preprint/technical report.

11. **Eq. (6), $\gamma$ derivation:** The 88.0 ms data portion calculation uses 2,112 bits (2,048 payload + 32 preamble + 16 header + 16 CRC), but the text says "preamble/sync (32 bits), header (16 bits), payload (2,048 bits), CRC-16 (16 bits)." The data portion should arguably exclude preamble/sync (which is overhead, not data), making $\gamma$ lower. Clarify the definition of $T_{\text{data}}$.

12. **Throughout:** The paper uses both "kbps" and "bps" without always specifying whether these are information bits or channel bits. At the MAC boundary ($1/\gamma$), this distinction matters.

---

## Overall Recommendation

**Major Revision**

The paper addresses a relevant problem and provides a well-structured analytical framework for hierarchical coordination sizing. The three-layer feasibility concept, the explicit superframe budget, and the design equations summary are useful contributions. However, the paper suffers from three fundamental issues that require substantial revision: (1) the DES provides negligible independent validation beyond what the closed-form equations already guarantee, creating a misleading impression of empirical rigor; (2) the most operationally critical constraint (TDMA superframe feasibility under half-duplex and GE losses) is never tested in simulation, leaving the paper's central sizing equations unvalidated at the physical layer they claim to bridge; and (3) the stress-case workload that drives the headline results is not operationally motivated. A major revision should either add packet-level validation of the TDMA frame model or substantially reframe the paper as a purely analytical sizing study with clearly bounded applicability. The topology comparison should be made fair or removed.

---

## Constructive Suggestions

1. **Add a slot-level analytical model for TDMA under GE losses.** Even without a full NS-3 simulation, the authors could extend the superframe budget (Table V) to account for wasted slots due to GE bad-state losses. This would quantify the interaction between GE losses and TDMA feasibility that the fluid-server DES cannot capture, and would strengthen the paper's most important practical result (the 623 ms margin).

2. **Lead with the event-driven profile as the primary result.** The $\eta_E \approx 6\%$ result under realistic operational assumptions is actually more impressive and useful than the $\eta_S \approx 46\%$ stress-case. Reframe the paper around the finding that hierarchical coordination adds only ~5–6% overhead under realistic conditions, with the stress-case as a parametric upper bound. This would also reduce the emphasis on the unicast staggering problem (Eq. 8), which applies only to an operationally questionable scenario.

3. **Provide empirical grounding for GE parameters.** Cite or derive GE parameters from LEO ISL link budgets. Even a simple link budget (transmit power, antenna gain, path loss at 500 km, receiver sensitivity, fade margin) would allow mapping physical obstruction scenarios to $(p_G, p_B, p_{GB}, p_{BG})$ ranges, transforming the sensitivity sweep from a parametric exercise into a physically grounded design tool.

4. **Reduce DES presentation; add a "what the DES uniquely provides" paragraph.** The DES's unique contributions are: (a) GE inter-cycle recovery tail statistics, (b) joint interaction verification (Table VI), and (c) confirmation that the closed-form equations are correctly implemented. State this explicitly and reduce the MC configuration details (seed strategy, runtime benchmarks, bootstrap CIs on deterministic quantities) that suggest more empirical content than exists.

5. **Develop the $\geq$10 kbps regime more thoroughly.** Since this is the nominal operating regime (optical ISLs), the paper should characterize what *does* become binding at higher rates—antenna scheduling, visibility constraints, inter-plane routing—even if only qualitatively. The current treatment ("all constraints are non-binding") is unsatisfying for a sizing paper; practitioners need to know what to size *next* after the message-layer constraints are resolved.