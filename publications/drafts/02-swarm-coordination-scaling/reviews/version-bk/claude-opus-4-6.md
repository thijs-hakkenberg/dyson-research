---
paper: "02-swarm-coordination-scaling"
version: "bk"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-27"
recommendation: "Major Revision"
---

# Peer Review: "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms"

**Manuscript Version:** BK
**Venue:** IEEE Transactions on Aerospace and Electronic Systems

---

## 1. Significance & Novelty

**Rating: 3 (Adequate)**

The paper addresses a genuine gap: there is no published work providing closed-form parametric sizing equations for hierarchical coordination architectures at the $10^3$–$10^5$ node scale with byte-level traffic accounting. The authors correctly identify that swarm robotics literature operates at 10–100 agents, constellation management at ~$10^4$, and networking literature treats routing but not coordination overhead budgets. The three-layer feasibility decomposition (byte budget, MAC efficiency, TDMA airtime) is a useful conceptual contribution for systems engineers.

However, the novelty is tempered by the nature of the results. The core finding—that architecture-specific overhead is ~5% while command traffic dominates—is essentially a bookkeeping exercise once the message model is fixed. The "closed-form equations" (e.g., Eq. 7 for AoI P99, Eq. 5 for coordinator ingress) are straightforward applications of geometric distributions and link budgets, not novel analytical derivations. The GE inter-cycle recovery analysis (Section IV-C) is the most technically interesting contribution, but Gilbert-Elliott models with Markov recovery are well-established in the communications literature. The paper's value lies more in the systematic application of known techniques to a specific architectural context than in methodological innovation.

The practical relevance is also somewhat unclear. The 1 kbps design point—which drives most of the interesting constraints—is acknowledged as an RF-backup edge case representing <1% of operational time. At the nominal ≥10 kbps regime, the authors themselves state "all constraints are non-binding" (Table I), which raises the question of whether the detailed TDMA frame analysis and coordinator bottleneck characterization are solving a problem that matters in practice.

## 2. Methodological Soundness

**Rating: 3 (Adequate)**

The methodology has several strengths: assumptions are explicitly stated, the message model is well-defined, the DES is described with sufficient detail for reproduction, and the Monte Carlo configuration (30 replications, bootstrap CIs) is appropriate. The open-source code availability is commendable. The three sanity-check models for coordinator ingress (TDMA, Model A probabilistic, Model B token bucket) converging to 20–50 kbps is a good validation practice.

However, there are fundamental methodological concerns:

**Circularity of validation.** The paper repeatedly emphasizes that the DES agrees with the closed-form equations to <0.1% (Table VI). But as acknowledged in Section V-A, both operate at the same message-layer abstraction. The DES is essentially re-implementing the same arithmetic with random seeds. This is implementation verification, not validation. The paper is transparent about this distinction, but the <0.1% agreement is then given undue prominence (abstract, multiple tables, conclusion) in a way that could mislead readers about the level of validation achieved.

**Message model rigidity.** The entire analysis rests on fixed message sizes (256 B status, 512 B commands, 64 B heartbeats, 128 B alerts) that are assumed rather than derived from mission requirements. No sensitivity analysis is performed on message sizes, despite these being the primary drivers of all overhead calculations. A 512 B command is asserted but never justified against actual command content for orbit adjustment or task assignment. Similarly, the 256 B status report containing "position, velocity, health, power, cluster" could plausibly range from 50 B (compressed state vector) to several kB (with covariance matrices).

**Static topology assumption.** While the authors bound re-association overhead at <0.5%, the static cluster membership assumption is problematic for LEO cross-plane configurations where the paper claims applicability. The 45–90 min re-association timescale means clusters are reconstituting multiple times per orbit. The quantitative bound in Section V-B ($f_h = 0.8\%$) considers only the fraction of nodes in transition at any instant but ignores the cumulative effect on coordinator state consistency and the interaction between re-association and GE loss events.

**GE model limitations.** The per-cycle coherence assumption (GE state constant within $T_c$) is acknowledged as conservative for recovery but is a strong simplification. More critically, the GE model is applied identically to all links in a cluster, whereas in reality, different member-to-coordinator links would have independent or spatially correlated channel states. The paper does not model the joint distribution of link states across cluster members, which matters for per-cycle cluster completion probability.

## 3. Validity & Logic

**Rating: 3 (Adequate)**

The internal logic is generally sound, and the authors are commendably transparent about limitations. The decomposition of overhead into architecture-specific ($\eta_0$) and workload-dependent ($\eta_{\text{cmd}}$) components is clean and well-justified. The observation that command traffic is topology-invariant (given centralized command generation) is an important insight that is correctly qualified with the caveat about alternative decision architectures.

Several logical issues deserve attention:

**The sectorized mesh comparison is problematic.** The capped sectorized mesh (cap = 10, 3.2% sector coverage) is compared against the hierarchy (100% cluster coverage) and found to be less bandwidth-efficient per peer. But this comparison conflates two architectures with fundamentally different functional scopes, as the authors acknowledge in Table IX. The $14\times$ efficiency claim (Section IV-G) is technically correct but misleading—it compares a local monitoring protocol against a full coordination architecture. The paper would be stronger if it either (a) designed a sectorized mesh variant with comparable functional scope, or (b) dropped the quantitative efficiency comparison and limited the discussion to qualitative trade-offs.

**Availability estimates lack rigor.** The 99.5% system availability figure (Section III-B, Table VIII) is derived from a "two-state Markov model" that is never fully specified. The MTTF = 50 yr and MTTR ≈ 35 s are stated but the interaction with coordinator election, cascading failures, and the triple-fault scenario is handled qualitatively. The degradation to ~99.2% under triple-fault is stated without derivation. For a paper focused on parametric sizing equations, the availability model should be as rigorous as the bandwidth model.

**Extrapolation beyond validated range.** Figure 9 includes a $10^6$-node curve labeled as "analytical extrapolation." While the caption notes this, the figure visually suggests validated scaling to $10^6$. The $O(N)$ scaling argument is sound in principle, but the static topology assumption becomes increasingly untenable at $10^6$ nodes, and the paper has not validated any results beyond $10^5$.

**The "stress case" framing.** The stress case ($\eta_S \approx 46\%$) assumes every node receives a 512 B command every cycle. This is presented as an upper bound, but no operational scenario is described that would generate this traffic pattern. If it represents a fleet-wide maneuver campaign, the duration would be finite and the steady-state analysis less relevant. If it represents routine operations, the 1 kbps budget is clearly inadequate regardless of architecture.

## 4. Clarity & Structure

**Rating: 4 (Good)**

The paper is generally well-written and well-organized. The roadmap at the beginning of Section IV is helpful. The notation table (Table I) is clear. The progressive disclosure of results—from single-factor analyses (IV-A through IV-C) to joint interaction (IV-D) to the design envelope (IV-E)—is logical.

Several aspects of the presentation could be improved:

**Excessive qualification and self-referencing.** The paper contains an unusual amount of defensive qualification, presumably in response to prior review rounds. Phrases like "this is the topology-dependent cost," "this is an intentional worst-case upper bound," and "all results are message-layer predictions" appear repeatedly. While transparency is valued, the repetition becomes distracting. For example, the statement that results are "message-layer" appears in the abstract, Section I-C, Section III-E, Section V-A, Section V-C, and the Conclusion.

**Table and figure density.** The paper contains 12 tables and 14 figures, which is excessive for a journal paper of this scope. Several could be consolidated or moved to supplementary material. Table VI, for instance, reports identical $\eta_{\text{DES}}$ values at all fleet sizes—the point could be made in one sentence. Tables IV and VII could be merged.

**The abstract is overloaded.** The abstract attempts to convey too many specific numerical results (η₀ ≈ 5%, η_E ≈ 6%, η_S ≈ 46%, 22-cycle staggering, 24 kbps, 623 ms margin, 440 s AoI P99, 4-cycle GE recovery, ≥10 kbps threshold). A more effective abstract would state the key insight (architecture overhead is small; command traffic dominates) and the primary design equations, leaving specific numbers to the body.

**Notation inconsistency.** $\eta$ is defined as "protocol overhead" in Table I but the text sometimes uses $\eta$ to include baseline telemetry and sometimes excludes it. The relationship $\eta_{\text{total}} = \eta + 20.5\%$ is stated multiple times but the switching between $\eta$ and $\eta_{\text{total}}$ in different tables creates confusion (e.g., Table I vs. Table V).

## 5. Ethical Compliance

**Rating: 4 (Good)**

The paper includes an appropriate acknowledgment of AI-assisted ideation in the Acknowledgment section, citing specific models (Claude 4.6, Gemini 3 Pro, GPT-5.2) and noting that the AI-generated concepts are "not validated here." The open-source code and data availability statement support reproducibility. The anonymous authorship ("Project Dyson Research Team") with a note about final publication is unusual but acceptable for review.

One concern: the reference to "Claude 4.6" and "GPT-5.2" suggests either future model versions or fictional version numbers (as of mid-2025). If these are actual tools used, the version numbers should be verifiable. If they are placeholders, this should be clarified.

The paper does not discuss potential dual-use concerns related to autonomous swarm coordination, which is relevant given the military applications cited (DARPA OFFSET, Blackjack, Replicator). While this is not strictly required, a brief acknowledgment would be appropriate for IEEE T-AES.

## 6. Scope & Referencing

**Rating: 3 (Adequate)**

The paper is appropriate for IEEE T-AES in topic, though the contribution level is borderline for this venue. The reference list is comprehensive (50+ references) and covers the relevant domains: constellation operations, swarm robotics, distributed systems, queueing theory, and AoI. Key foundational works are cited (Kleinrock, Lamport, Raft, SWIM, AoI framework).

Several referencing concerns:

**Non-archival sources.** Multiple references are to non-archival sources: SpaceX FCC filings, Amazon web pages, DARPA program pages, DoD fact sheets, and "Jonathan's Space Report." While some of these are unavoidable for current constellation data, the paper should minimize reliance on non-archival sources for technical claims.

**Missing relevant work.** The paper does not cite several relevant bodies of work: (a) the extensive literature on satellite network topology design and optimization (e.g., Ekici et al., IEEE JSAC 2001); (b) recent work on distributed satellite autonomy beyond NASA DSA (e.g., ESA's OPS-SAT experiments); (c) the CCSDS Spacecraft Onboard Interface Services (SOIS) standards, which are directly relevant to the inter-node communication model; (d) recent AoI work specifically in satellite networks (e.g., satellite-IoT AoI optimization papers from 2022–2024).

**Self-citation.** Reference [39] (dyson_multimodel) is a self-citation to an unpublished work at the project's own URL. This is acceptable for methodology disclosure but should not be relied upon for technical claims.

---

## Major Issues

1. **No physical-layer validation and limited practical relevance of the design-driving case.** The entire analysis operates at the message layer, and the design-driving 1 kbps case applies to <1% of operational time. The paper acknowledges this but does not adequately address why the community should care about detailed TDMA frame budgets for an edge case. Either (a) provide at least a single-cluster NS-3 validation to demonstrate that message-layer predictions hold under realistic PHY conditions, or (b) reframe the contribution around the ≥10 kbps nominal case and treat the 1 kbps case as a brief robustness check.

2. **Message size sensitivity is absent.** All overhead calculations are deterministic functions of fixed message sizes. No sensitivity analysis explores how results change if status reports are 128 B or 512 B, or if commands are 256 B or 1024 B. Given that message sizes are the primary free parameters and are assumed rather than derived, this is a significant gap. At minimum, provide a parametric sweep over message sizes analogous to the $\gamma$ sensitivity in Fig. 12.

3. **The DES "validation" overstates confidence.** The <0.1% DES-analytic agreement is prominently featured but represents implementation verification of identical assumptions, not independent validation. The paper should (a) reduce the prominence of this metric, (b) clearly label it as "implementation consistency check" rather than "verification," and (c) identify what independent evidence (hardware-in-the-loop, packet-level simulation, or operational data) would constitute actual validation.

4. **Incomplete availability model.** The 99.5% availability claim is not derived with the same rigor as the bandwidth equations. The two-state Markov model is never written down. Cascading failure probability (coordinator failure triggering cluster degradation) is not quantified. The interaction between coordinator duty cycle, failure rate, and GE channel state is not analyzed jointly.

## Minor Issues

1. **Eq. 2 ($W_q$):** The M/D/1 waiting time formula is correct but the paper should note this is the Pollaczek-Khinchine result specialized to deterministic service ($C_s^2 = 0$), since the general P-K formula is $W_q = \rho(1 + C_s^2)/(2\mu_s(1-\rho))$.

2. **Section III-B (Hierarchical Topology):** The Raft election description states "quorum = $k_c/2 + 1 = 51$ responders required" but Raft elections require a majority of the *voting members*, which in a cluster of 100 would be 51 votes total (including the candidate's self-vote), meaning 50 external responses. This is a minor point but should be precise.

3. **Table II (Simulation Parameters):** The collision avoidance rate of $10^{-4}$/node/s yields ~10 alerts/s fleet-wide at $N = 10^5$, or ~100 per $T_c$. The footnote says these are "screening notifications" but the 128 B message size and Poisson model should be justified against actual conjunction screening cadences (ESA reports ~100 warnings/week for the current catalog, not per second).

4. **Eq. 6 ($B_{\text{sector}}^{\text{capped}}$):** The equation uses $\min(k_s - 1, 10)$ but the text later states cap = 10 is the default. For $N \geq 121$ (where $k_s \geq 11$), the min is always 10, making the formula simply $256 + 320 = 576$ B. The generality of the min() is unnecessary for the parameter range studied.

5. **Table III footnote (a):** The analytical formula for $\eta_{\text{sector}}$ includes 512 B for commands, but the sectorized mesh has no coordinator to issue commands (Table IX shows "---" for fleet command dissemination). This inconsistency inflates the sectorized mesh overhead.

6. **Section IV-A:** "Fleet-wide TDMA cost is 0.28 kbps/node (1% coordinators)" — this calculation is not shown and the 1% figure assumes exactly $N/k_c$ coordinators with $k_c = 100$. State this explicitly.

7. **Figure 9 caption:** States the $10^6$ curve is "analytical extrapolation" but the figure axis label should also indicate this (e.g., with a different line style clearly distinguished in the legend).

8. **Acknowledgment section:** "Claude 4.6, Gemini 3 Pro, GPT-5.2" — verify these are actual model version identifiers. If the paper is set in a near-future context, this should be noted.

9. **Data Availability:** The GitHub tag `paper-02-v-bk` is specific and good practice. Consider adding a Zenodo DOI for long-term archival.

10. **Throughout:** The paper uses "coordinator" to mean both the cluster-level and regional-level nodes. While context usually disambiguates, explicit qualification (e.g., "cluster coordinator") would improve clarity in Sections IV-A and IV-D.

## Overall Recommendation

**Major Revision**

This paper addresses a legitimate gap in the literature and provides a systematic, well-documented framework for sizing hierarchical coordination architectures at scale. The three-layer feasibility decomposition, the GE inter-cycle recovery analysis, and the TDMA superframe budget are useful contributions for spacecraft systems engineers. However, the paper suffers from three fundamental issues that prevent acceptance in its current form: (1) the absence of any physical-layer validation means the results are self-consistent predictions, not validated design equations—the title's promise of "design equations" implies a level of engineering utility that message-layer-only analysis cannot deliver; (2) the insensitivity to message sizes, which are the primary free parameters, undermines the parametric nature of the contribution; and (3) the design-driving 1 kbps case is an edge condition where the detailed analysis may not justify the complexity, while the nominal ≥10 kbps case renders most constraints non-binding. A major revision addressing these issues—particularly adding message-size sensitivity and either a packet-level validation or a reframing of scope—would substantially strengthen the paper.

## Constructive Suggestions

1. **Add message-size sensitivity analysis.** Sweep status report size (128–512 B), command size (256–1024 B), and heartbeat size (32–128 B) and present the resulting $\eta_0$ and $\eta_{\text{cmd}}$ ranges. This would transform the fixed-parameter accounting into genuinely parametric design equations and is achievable with the existing DES infrastructure.

2. **Perform a single-cluster NS-3 simulation.** Table VII provides the TDMA superframe specification. Implementing a 100-node TDMA cluster in NS-3 with realistic PHY (including preamble detection, CRC failure, half-duplex switching) would provide the first physical-layer data point. Even a single configuration ($k_c = 100$, 24 kbps, GE channel) showing that message-layer predictions hold within X% would dramatically strengthen the paper's claims.

3. **Rebalance the presentation around the nominal regime.** Currently, the 1 kbps RF-backup case dominates the analysis while the ≥10 kbps nominal case is dismissed as "non-binding." Consider restructuring: lead with the nominal case (showing that hierarchical coordination is lightweight at practical bandwidths), then present the 1 kbps analysis as a degraded-mode robustness characterization. This would better serve practitioners who need to know both the normal operating point and the failure-mode floor.

4. **Formalize the availability model.** Write down the continuous-time Markov chain for cluster availability (states: nominal, election-in-progress, degraded, failed) with explicit transition rates derived from the failure model, election duration, and GE parameters. Derive the 99.5% figure analytically and provide sensitivity to failure rate and $p_{BG}$.

5. **Reduce redundancy and consolidate tables.** The paper could be shortened by ~20% without losing content. Merge Tables IV and VII (both address sectorized mesh parameters). Consolidate the repeated "message-layer only" caveats into a single prominent boxed statement. Move Tables V and VI to an appendix or supplementary material, replacing them with a single sentence stating the key result.