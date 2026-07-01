---
paper: "02-swarm-coordination-scaling"
version: "bm"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-27"
recommendation: "Major Revision"
---

# Peer Review: "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms"

## 1. Significance & Novelty
**Rating: 3 (Adequate)**

The paper addresses a genuine gap: there is no published work providing closed-form parametric sizing equations for coordination architectures spanning $10^3$–$10^5$ autonomous space nodes with byte-level traffic accounting. The authors correctly identify that swarm robotics literature operates at 10–100 agents, constellation management at ~$10^4$, and networking literature treats routing but not coordination overhead budgeting. The three-layer feasibility framework (byte budget, MAC efficiency, TDMA airtime) is a useful conceptual contribution that practitioners could apply.

However, the novelty is tempered by the fact that the "closed-form equations" are relatively straightforward accounting identities rather than deep analytical results. Equation (4) for hierarchical messages is a simple fan-out sum; Equation (7) for AoI P99 is a standard geometric quantile; the GE recovery CDF is a textbook Markov chain calculation. The intellectual contribution lies more in the systematic assembly and parameterization of these known results into a coherent sizing framework than in any individual analytical advance. This is valuable engineering work, but the paper occasionally overstates the difficulty of the derivations.

The central finding—that architecture-specific overhead ($\eta_0 \approx 5\%$) is small while command traffic dominates—is useful but somewhat predictable once the message sizes are specified. The more interesting result is the three-layer feasibility distinction showing that stress-case unicast commands pass byte-budget and MAC layers but fail the airtime layer, requiring 22-cycle staggering. This kind of multi-layer feasibility analysis is the paper's strongest conceptual contribution.

## 2. Methodological Soundness
**Rating: 3 (Adequate)**

The methodology has a fundamental circularity that the authors partially acknowledge but do not fully resolve: the DES and the closed-form equations operate at the same abstraction level, so the <0.1% agreement (Table VI) confirms implementation consistency, not model validity. The authors state this explicitly (Section V-A), which is commendable, but the paper's title and framing ("Design Equations") implies a level of engineering utility that requires physical-layer grounding the paper does not provide.

The cycle-aggregated DES design is appropriate for the message-layer questions asked, and the 30-replication Monte Carlo with bootstrap CIs is statistically adequate. However, several methodological choices deserve scrutiny:

- **The fluid-server ingress model in the DES** (Section III-A, step 5) does not enforce TDMA slot scheduling, yet the paper's primary coordinator sizing result (24 kbps) is derived from TDMA analysis. The paper acknowledges this mismatch (Section IV-D, "Model enforcement note") but the disconnect means the DES cannot validate the most operationally critical result—whether the TDMA superframe actually works under realistic arrival patterns with retransmissions.

- **The GE coherence assumption** (state constant within $T_c$) is stated to be conservative for recovery but is not validated against any physical channel model. The authors provide a useful physical mapping (Section IV-C) identifying three obstruction mechanisms, but the claim that the model provides "an upper bound on recovery time" is only true if the coherence time exceeds $T_c$—which they acknowledge may not hold for structural shadowing ($\tau_c \approx 1$–10 s).

- **Static cluster membership** for a 1-year simulation of LEO constellations is a significant simplification. The quantitative bound ($f_h = 0.8\%$ of nodes in handoff transient) is helpful but assumes the re-association process itself works correctly—which has not been simulated.

The MAC efficiency parameter $\gamma$ serves as a catch-all for unmodeled physical-layer effects. While the sensitivity analysis over $\gamma \in [0.7, 0.9]$ is useful, the derived value of $\gamma = 0.949$ (Eq. 6) versus the conservative $\gamma = 0.85$ used throughout creates ambiguity about which regime the results actually apply to. The gap between 0.85 and 0.949 is attributed to "FEC coding (~7%), ranging/calibration (~3%), and control-channel overhead (~5%)" but these are rough estimates that sum to 15%, not the 10% difference between the two $\gamma$ values.

## 3. Validity & Logic
**Rating: 3 (Adequate)**

The internal logic of the paper is generally sound, and the authors are commendably transparent about limitations. The three-layer feasibility framework (Table V) is logically coherent, and the distinction between broadcast and unicast command dissemination (Type 1 vs. Type 2) is well-handled. The identification that stress-case unicast fails Layer 3 while passing Layers 1–2 is a genuinely useful design insight.

Several logical issues merit attention:

**The topology comparison is asymmetric and potentially misleading.** The centralized baseline models only compute-queue scalability (M/D/c), not communication overhead; the global-state mesh is an intentional worst case; the sectorized mesh has narrower functional scope. The authors acknowledge all of this (Table VII footnotes, Table VIII), but the visual presentation (Fig. 10) and the "14× bandwidth efficiency per unit of awareness" claim (Section IV-G) invite readers to draw comparisons that the authors themselves caution against. The normalized cost-per-peer metric ($0.46\%$/peer vs. $6.5\%$/peer) is misleading because it divides by different denominators (100 peers vs. 10 peers) from architectures providing qualitatively different services.

**The coordinator failure analysis** (Section III-B.2) is thorough for single and double faults but the triple-fault probability calculation ($0.02 \times 0.01 \times 0.09 = 1.8 \times 10^{-5}$/yr) assumes independence of events that the text itself notes may be correlated ("power-negative or tumbling" causing both coordinator failure and optical outage). If these events are correlated, the probability could be orders of magnitude higher.

**The claim that "at ≥10 kbps, all constraints are non-binding"** (Abstract, Table I, Section I-C) is true only within the message-layer model. The authors note that "currently unmodeled constraints (antenna scheduling, visibility, interference) may become binding" but this caveat is insufficiently prominent given the strength of the claim.

**Table IV (Joint Interaction):** The identical "No Loss" and "GE Only" drop columns are presented as evidence of pipeline decoupling, but this is an artifact of the fluid-server model—lost messages never enter the queue. Under TDMA (where corrupted packets consume slot time), this decoupling would not hold, as the authors note. The table therefore validates a property of the DES implementation, not of the physical system.

## 4. Clarity & Structure
**Rating: 4 (Good)**

The paper is well-organized and generally well-written. The roadmap at the beginning of Section IV is helpful. The notation table (Table I) is clear and consistently used. The three-layer feasibility framework provides a useful organizing principle. The extensive use of cross-references between sections helps readers navigate the dense material.

The paper is, however, extremely dense—arguably too dense for a journal paper. There are 12 tables, 14 figures, and numerous inline calculations. Some material could be moved to supplementary material without loss of the main argument. The superframe time budget (Table III), the sector-cap sensitivity sweep (Table II in Section III), and the duty-cycle trade-offs (Table IX) are useful reference material but interrupt the flow of the primary contributions.

The abstract is accurate but packed with specific numbers that may overwhelm readers unfamiliar with the framework. The key message—that architecture-specific overhead is small (~5%) while command traffic dominates—could be stated more prominently before diving into specific values.

One structural concern: the paper intermixes model description (Section III) with results that depend on parameter choices not yet justified. For example, the sectorized mesh model (Section III-B.4) includes Table II with overhead percentages that are results, not model parameters. Similarly, the coordinator failure transient analysis in Section III-B.2 reads more like a results subsection.

The figures are referenced appropriately but are not included in the review (PDF not provided). Based on captions, they appear well-designed with appropriate annotations.

## 5. Ethical Compliance
**Rating: 4 (Good)**

The paper includes an explicit acknowledgment of AI-assisted ideation (Claude 4.6, Gemini 3 Pro, GPT-5.2) with a citation to a methodology paper and the clear statement that the AI-generated concepts "are not validated here." This is transparent and appropriate. The anonymous authorship ("Project Dyson Research Team") with a note that individual names will be provided for final publication is acceptable for review but must be resolved before publication per IEEE policy.

The open-source code availability (GitHub with specific tag) and detailed parameter tables support reproducibility. The Monte Carlo configuration (30 replications, sequential Mersenne Twister seeds) is fully specified. The total wall-clock time (~90 min) and hardware requirements (commodity) lower the barrier to reproduction.

One minor concern: the reference to future model versions (Claude 4.6, GPT-5.2) suggests these may be hypothetical or unreleased models, which could confuse readers about the timeline of the work. This should be clarified.

## 6. Scope & Referencing
**Rating: 3 (Adequate)**

The paper is appropriate for IEEE T-AES in scope, addressing autonomous spacecraft coordination at scale. The reference list (50 entries) covers the major relevant areas: constellation operations, swarm robotics, distributed systems theory, queueing theory, and space standards.

However, several gaps exist:

- **No references to existing space network simulation tools** (e.g., STK, GMAT, or academic constellation simulators) that could provide the physical-layer validation the paper identifies as future work.

- **Limited engagement with the DTN/space networking community** beyond the Cerf RFC and BPv7 standard. The Contact Graph Routing literature (Fraire et al., 2021) is directly relevant to scheduled access in space networks and is not cited.

- **No references to operational ISL scheduling work** from Starlink or similar programs, despite ISL scheduling being identified as a key unmodeled constraint.

- **The O'Neill (1976) and Badescu (2006) references** for $10^5$–$10^6$ unit concepts are speculative and decades old. More recent references to actual mega-constellation filing trends (ITU filings, FCC applications) would strengthen the motivation.

- Several references are non-archival (Amazon Kuiper overview, DARPA program pages, DoD fact sheets). While unavoidable for some operational programs, the paper should minimize reliance on these for substantive claims.

---

## Major Issues

1. **Validation gap undermines the "Design Equations" framing.** The paper's title and abstract promise "design equations" for engineering use, but all results are message-layer predictions validated only against a DES at the same abstraction level. The <0.1% DES-analytic agreement demonstrates algebraic correctness, not engineering validity. The paper needs either (a) at least one physical-layer validation point (even a simplified NS-3 single-cluster experiment) or (b) a significantly more cautious framing that positions these as "message-layer sizing estimates" rather than "design equations." The current framing, while hedged in the text, is misleading in the title and abstract.

2. **The DES does not validate the primary engineering result.** The coordinator ingress sizing (24 kbps TDMA) is the most operationally actionable result, but the DES uses fluid-server ingress, not TDMA slot scheduling. The superframe time budget (Table III) is purely analytical. The 623 ms margin at 24 kbps (shrinking to 98 ms at $\gamma = 0.80$) is uncomfortably tight for a system with no physical-layer validation. The paper should either implement TDMA scheduling in the DES or clearly state that the superframe feasibility is an unvalidated analytical prediction.

3. **Asymmetric topology comparison.** The four topologies are modeled at different levels of fidelity and provide different functional capabilities, yet are compared in the same figures and tables. The centralized model captures only compute queuing; the global-state mesh is an intentional strawman; the sectorized mesh provides only local monitoring. Only the hierarchical architecture is fully modeled at the communication layer. The paper should restructure the comparison to clearly separate (a) the hierarchical sizing results (the primary contribution) from (b) the topology comparisons (which are illustrative bounds, not apples-to-apples comparisons).

4. **The 1 kbps design point needs stronger justification.** The paper acknowledges that 1 kbps is an RF-backup edge case applying <1% of operational time, yet the majority of results and all binding constraints are presented at this rate. The claim that this is "design-driving" is reasonable for safe-mode sizing but the paper should present the 10 kbps nominal case with equal prominence, since that is where the system operates >99% of the time. Currently, the 10 kbps case is dismissed in one sentence ("all constraints are non-binding") without exploring what *does* become binding at that rate.

5. **GE model coherence assumption lacks physical grounding.** The per-cycle GE state transition (constant within $T_c = 10$ s) is a modeling convenience, not a physical channel model. For LEO ISLs, the relevant obstruction mechanisms have coherence times ranging from ~1 s (structural shadowing) to ~35 min (Earth occultation). The paper's claim that the model provides "an upper bound on recovery time" holds only for the subset of obstruction mechanisms with $\tau_c > T_c$. A sensitivity analysis over GE transition granularity (sub-cycle transitions) would significantly strengthen the results.

---

## Minor Issues

1. **Eq. (2), M/D/1 waiting time:** The formula $W_q = \rho / (2\mu_s(1-\rho))$ is the Pollaczek-Khinchine result for M/D/1, but the notation is slightly non-standard. Clarify that $\mu_s$ here is the service rate, not the mean service time.

2. **Section III-B.2, Raft election over RF:** "51 × 0.8 s = 41 s at 1 kbps under Slotted ALOHA" — the 0.8 s per response assumes 100 B × 8 / 1000 bps = 0.8 s, but Slotted ALOHA throughput is ~36% of channel capacity, so effective per-message time should be ~2.2 s, giving ~112 s total. The calculation appears to use raw bit rate, not Slotted ALOHA effective throughput.

3. **Table I notation:** $\eta_{\text{total}}$ is defined as $\eta + 20.5\%$ baseline, but the 20.5% itself is defined later in Section III-E. Forward-reference or reorder.

4. **Section III-B.3, Eq. (5):** The gossip fanout $f = N/\log N$ is described as "aggressive" but is actually the standard choice for single-round convergence in epidemic protocols. The characterization as "aggressive" may confuse readers familiar with gossip literature.

5. **Table VI:** The note "η_DES = 46.0% at all 8 intermediate sizes (5k–80k); omitted for brevity" should either show at least 2–3 intermediate points or be presented as a figure showing the flat scaling.

6. **Section IV-A, "Model A" Monte Carlo:** "Monte Carlo estimate from $10^5$ random arrival patterns" — this is a separate MC from the main 30-replication DES. Clarify whether this uses the same random number infrastructure and whether results are reproducible from the published code.

7. **Eq. (8), unicast stagger:** $\alpha_{\text{RX}}$ is used but not formally defined until Eq. (9). Define at first use.

8. **Section IV-G, "14× difference in bandwidth efficiency per unit of awareness":** This metric conflates bandwidth overhead with functional scope in a way that favors the hierarchy. A fairer comparison would normalize by the number of *unique* peers monitored per unit overhead, acknowledging that the hierarchy's 100-peer awareness includes coordinator-mediated indirect awareness while the mesh's 10-peer awareness is direct.

9. **Bibliography:** References [5] (O'Neill 1976) and [6] (Badescu 2006) are used to motivate $10^5$–$10^6$ unit scales but are speculative futurism, not engineering references. Consider replacing or supplementing with ITU/FCC mega-constellation filings.

10. **Section V-B, re-association overhead:** The bound $f_h = \lambda_h \times t_h = 0.8\%$ assumes a single handoff per boundary crossing. If clusters are small relative to orbital velocity, a node might cross multiple cluster boundaries per orbit, increasing $\lambda_h$.

11. **Abstract:** "open-source Monte Carlo tool verifies equation consistency to <0.1%" — this phrasing implies independent validation. Rephrase to "confirms implementation consistency" to avoid overstating.

12. **Throughout:** The paper uses both "kbps" and "bps" without always being explicit about whether these are information rates or channel rates. Standardize.

---

## Overall Recommendation

**Major Revision**

This paper presents a systematic and carefully documented message-layer sizing framework for hierarchical coordination in large autonomous space swarms. The three-layer feasibility framework, the workload design envelope, and the GE inter-cycle recovery characterization are useful contributions. The authors are commendably transparent about limitations, and the open-source code supports reproducibility.

However, the paper suffers from a fundamental gap between its claims ("Design Equations") and its validation level (message-layer self-consistency only). The DES does not validate the most operationally critical result (TDMA superframe feasibility), the topology comparison is asymmetric, and the 1 kbps design point—while justified as an edge case—dominates the presentation at the expense of the nominal operating regime. A major revision should (1) reframe the contribution as message-layer sizing estimates pending physical-layer validation, (2) either add a minimal TDMA-scheduled DES or clearly flag the superframe budget as unvalidated, (3) restructure the topology comparison to avoid misleading cross-architecture claims, and (4) give the ≥10 kbps regime equal analytical treatment.

---

## Constructive Suggestions

1. **Implement TDMA slot scheduling in the DES for at least one configuration** ($k_c = 100$, 24 kbps, GE channel). This would validate the superframe time budget (Table III) and the half-duplex TX/RX partitioning—the paper's most operationally critical predictions. Even a simplified slot-level model (without full PHY) would substantially strengthen the contribution. If this is infeasible, present the superframe analysis as a "design specification for future validation" rather than a result.

2. **Present the ≥10 kbps regime as a co-equal results section**, not a dismissive one-liner. At 10 kbps, what *does* become the binding constraint? Antenna scheduling? Visibility windows? Inter-plane handoff? Even a qualitative analysis of the next binding constraint beyond the message layer would significantly increase the paper's practical value for constellation designers who will operate at 10+ kbps.

3. **Restructure the topology comparison** into two tiers: (a) the hierarchical sizing results as standalone design equations (the primary contribution), and (b) a clearly labeled "illustrative comparison" section that presents the centralized, mesh, and sectorized baselines as bounding cases with explicit caveats about asymmetric modeling fidelity. Remove or heavily caveat the "14× efficiency" claim.

4. **Add a sub-cycle GE sensitivity analysis.** Partition each $T_c$ into $n$ sub-intervals with independent GE transitions and show how intra-cycle recovery improves as $n$ increases from 1 (current model) to 10. This would bound the conservatism of the per-cycle coherence assumption and provide practitioners with guidance on when the current model over- or under-estimates recovery.

5. **Tighten the abstract and title.** Replace "Design Equations" with "Message-Layer Sizing Equations" or "Parametric Sizing Estimates." In the abstract, lead with the conceptual contribution (three-layer feasibility framework) before the specific numbers. The current abstract reads like a technical summary for readers already familiar with the framework; it should first motivate why this framework matters.