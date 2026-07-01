---
paper: "02-swarm-coordination-scaling"
version: "bu"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-27"
recommendation: "Major Revision"
---

# Peer Review: "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms"

**Manuscript Version:** BU
**Venue:** IEEE Transactions on Aerospace and Electronic Systems

---

## 1. Significance & Novelty

**Rating: 3 (Adequate)**

The paper addresses a genuine gap: there is no published work providing closed-form parametric sizing equations for hierarchical coordination architectures at the $10^3$–$10^5$ node scale with byte-level traffic accounting. The authors correctly identify that swarm robotics literature operates at tens-to-hundreds of agents, constellation management addresses ~$10^4$ nodes without byte-level accounting, and networking literature treats routing without coordination overhead analysis. The three-layer feasibility framework (byte budget, MAC efficiency, TDMA airtime) is a useful conceptual contribution that practitioners could apply.

However, the novelty is more incremental than the framing suggests. The core analytical results—that $\eta$ is $O(1)$ in a tree hierarchy with fixed fan-out, that coordinator ingress is the bottleneck, and that GE correlated loss defeats intra-cycle retransmission—are relatively straightforward consequences of the assumed message model. The $O(1)$ overhead result follows directly from the fixed $k_c$ and fixed message sizes; the coordinator ingress sizing is a basic multiplexing calculation; the GE result is a known property of bursty channels. The paper's value lies in assembling these into a coherent design framework with specific numerical parameters, but the individual analytical contributions are modest.

The claim "to our knowledge, no prior work provides closed-form parametric sizing relationships" (Section I-A) is difficult to verify and somewhat narrow—LEACH and its descendants (which the authors cite) do provide cluster-head overhead analysis, albeit for terrestrial WSNs. The distinction is the space ISL context and the specific byte-level accounting, which is useful but not a fundamental methodological advance. The paper would benefit from more clearly positioning itself as a *systems engineering design tool* rather than implying deeper theoretical novelty.

## 2. Methodological Soundness

**Rating: 3 (Adequate)**

The methodology has a fundamental circularity that the authors partially acknowledge but do not fully resolve: the DES and the closed-form equations operate at the same abstraction level, so the <0.1% agreement (Table VII) confirms only that the DES correctly implements the equations, not that the equations capture physical reality. The authors state this explicitly (Section V-A), which is commendable, but it means the paper's primary validation mechanism is essentially a unit test. The DES provides independent value only for tail statistics (GE inter-cycle recovery), where the Markov chain prediction is also analytical.

**Specific methodological concerns:**

- **The GE model coherence assumption** (Section IV-C): fixing GE state for the entire $T_c = 10$~s cycle and allowing transitions only at cycle boundaries is a strong assumption that makes intra-cycle retransmission ineffective *by construction*. The authors acknowledge this but claim it is "conservative for recovery." This is true only if physical coherence times exceed $T_c$; for structural shadowing ($\tau_c \approx 1$–$10$~s, per the authors' own physical mapping), the coherence time may be shorter than $T_c$, making the model *optimistic* for burst duration. The claim of an "upper bound on recovery time" is therefore not uniformly valid.

- **The fluid-server DES vs. TDMA analytical check** creates a methodological gap: the DES does not enforce TDMA slot scheduling or half-duplex partitioning (acknowledged in Section IV-D), yet these are the binding constraints at 1 kbps. The joint interaction verification (Table V) is therefore incomplete—it validates fluid-server behavior but not the actual TDMA regime that the paper recommends.

- **Monte Carlo configuration**: 30 replications is adequate for mean estimation but marginal for P99 tail statistics. The authors compute per-run P99 over ~$3.15 \times 10^6$ samples and report the mean of 30 per-run values—this is reasonable but the bootstrap CI width should be reported for all tail statistics, not just AoI.

- **The $\sqrt{N}$ sector sizing** (Section III-B.4) is described as "an order-of-magnitude heuristic" derived from orbital density arguments. This is insufficiently justified for a paper claiming closed-form design equations. The conjunction screening volume argument needs a derivation or citation.

## 3. Validity & Logic

**Rating: 3 (Adequate)**

The core conclusions are internally consistent and follow from the assumptions. The decomposition $\eta = \eta_0 + \eta_{\text{cmd}}$ is clean and well-supported. The finding that architecture-specific overhead is small (~5%) while command traffic dominates the stress case is clearly demonstrated. The three-layer feasibility framework is logically sound.

**However, several logical issues weaken the analysis:**

1. **The stress-case workload definition** (Section IV-E) assumes every node receives a 512-byte command every cycle. This is presented as bounding "fleet-wide reconfiguration campaigns," but no evidence is provided that such campaigns actually require per-node-per-cycle commands. The 22-cycle unicast stagger result (Eq. 10) is a direct consequence of this assumption. If the stress case is unrealistic, the most dramatic results in the paper lose practical relevance.

2. **The centralized baseline comparison** (Table VIII, Fig. 8) is problematic. The centralized model captures only compute-queue scalability ($M/D/c$), not communication overhead. The authors acknowledge this (footnote d, Table VIII) but still include centralized curves in comparative figures (Fig. 8), which could mislead readers into thinking the hierarchy offers communication overhead advantages over centralized architectures. The paper should either model centralized communication overhead or remove centralized curves from overhead comparison figures entirely.

3. **The sectorized mesh comparison** is carefully qualified (Table IX, Section III-B.4) but the "14× bandwidth efficiency per unit of awareness" claim (Section IV-G) conflates two architectures with fundamentally different functional scopes. This metric is novel but potentially misleading—it assumes awareness of cluster peers and local neighbors are substitutable goods, which depends entirely on the application.

4. **The 1 kbps design point**: The paper argues this is the "design-driving edge case" (Section III-E) because it determines survival during optical outages. This is reasonable, but the paper then spends the majority of its analysis on this regime. If optical ISLs are available >99% of the time and all constraints are non-binding at ≥10 kbps (Table II), the practical relevance of the detailed 1 kbps analysis is limited to safe-mode design—which should be stated more prominently.

## 4. Clarity & Structure

**Rating: 4 (Good)**

The paper is generally well-organized and clearly written. The roadmap at the beginning of Section IV is helpful. The notation table (Table I) is well-placed. The three-layer feasibility framework provides a clear organizing principle. The design equations summary (Section V-C) is a valuable practitioner reference.

**Strengths:** The paper is unusually transparent about its limitations and modeling assumptions. The explicit statements about what the DES does and does not model (Section III-A, III-D), the validation gap discussion (Section V-A), and the careful qualification of cross-architecture comparisons are exemplary.

**Weaknesses:** The paper is excessively long for the analytical content it delivers. Much of the length comes from exhaustive qualification of every result, which—while intellectually honest—makes the paper difficult to read. The superframe time budget (Table IV), TDMA synchronization discussion, guard-time sensitivity, and half-duplex TX/RX partitioning could be condensed significantly. Section IV-A alone spans nearly 2 full pages of dense text for what is fundamentally a capacity calculation.

The paper also suffers from notational overload. The reader must track $\eta$, $\eta_0$, $\eta_{\text{cmd}}$, $\eta_{\text{total}}$, $\eta_{\text{eff}}$, $\eta_E$, $\eta_S$, $\eta_{\text{sector}}$, $\eta_{\text{sync}}$—nine overhead variants. A consolidated notation with fewer symbols and a single comprehensive table would improve readability.

Figures are referenced but not included (understandable for a LaTeX source review). The figure captions are informative and suggest the figures would be effective.

## 5. Ethical Compliance

**Rating: 4 (Good)**

The AI-assistance disclosure in the Acknowledgment section is appropriate and specific ("Claude 4.6, Gemini 3 Pro, GPT-5.2"), with a citation to a methodology paper. The statement that the AI-assisted ideation "is not validated here" is honest. The anonymous authorship ("Project Dyson Research Team") with a note that individual names will be provided for final publication is acceptable for review but must be resolved before publication per IEEE policy.

The open-source data availability statement with a specific repository tag is commendable and supports reproducibility. The parameter tables are sufficiently detailed for independent replication.

One minor concern: the Acknowledgment references "Claude 4.6" and "GPT-5.2," which do not exist as of my knowledge. If these are fictional model names used as placeholders, this should be clarified; if they refer to future models, the paper's timeline should be consistent.

## 6. Scope & Referencing

**Rating: 3 (Adequate)**

The paper is appropriate for IEEE TAES in scope, addressing autonomous spacecraft coordination at scale. The reference list (50+ citations) is comprehensive and covers the relevant domains: constellation operations, swarm robotics, distributed systems theory, queueing theory, AoI, and space communication standards.

**Concerns:**

- Several references are non-archival (Amazon Kuiper overview, DARPA program pages, DoD fact sheets, NRL magazine article). While some of these are unavoidable for operational programs, the paper relies on them for claims about the state of practice. At minimum, [3] (Kuiper), [20] (OFFSET), [22] (Replicator), [23] (NRL), and [36] (Blackjack) should be flagged as non-peer-reviewed.

- The LEACH citation [50] is appropriate but the comparison to LEACH is superficial. A more detailed discussion of how the coordinator rotation model differs from LEACH cluster-head selection (beyond the one-sentence mention in Section II-B) would strengthen the related work.

- Missing references: The paper does not cite key works on satellite constellation autonomy by Bonnet and Tessier (2009, AAMAS), or the extensive literature on distributed task allocation in multi-robot systems (e.g., Gerkey and Matarić, 2004). The mean-field game citations [16, 17] are included but not connected to the paper's results.

- The paper cites "Castet and Saleh, 2009" [29] for the 2%/year failure rate and 50-year MTTF. This reference covers historical satellite reliability data; the 50-year MTTF may not be representative of the small-satellite/CubeSat platforms likely used in $10^5$-node swarms. This assumption should be discussed.

---

## Major Issues

1. **No physical-layer validation of any kind.** The paper's central results (coordinator ingress sizing, TDMA feasibility, superframe margin) depend critically on $\gamma$, which is assumed rather than validated. The DES does not model MAC contention, and the TDMA frame analysis (Section IV-A) is purely analytical. The 623 ms superframe margin at $\gamma = 0.85$ shrinks to 98 ms at $\gamma = 0.80$—a regime where unmodeled effects (ranging, FEC, control-channel overhead) could easily consume the margin. The paper acknowledges this but does not provide even a simple sensitivity analysis of what happens when the margin goes negative. **Required:** Either provide a packet-level simulation of a single cluster (even simplified), or significantly downgrade the claims about TDMA feasibility and present the superframe budget as a *specification for future validation* rather than a *result*.

2. **The DES validates the equations, not the physics.** The <0.1% agreement is presented as a key result (Table VII, abstract), but it is a tautological verification—the DES implements the same message-layer model as the equations. The paper needs to be restructured to make clear that the DES provides value only for: (a) tail statistics not easily derived analytically, and (b) joint interaction verification. The current framing overstates the DES's role.

3. **The stress-case workload lacks operational justification.** The 512 B/node/cycle command rate that drives $\eta_S \approx 46\%$ and the 22-cycle unicast stagger is not grounded in any operational scenario analysis. What constellation operation requires every node to receive a unique 512-byte command every 10 seconds for sustained periods? Without this justification, the stress case may be an unrealistic bound that inflates the paper's apparent contribution. **Required:** Either cite operational data supporting this command rate, or present it explicitly as a parametric upper bound with a discussion of realistic command rates.

4. **Inconsistent treatment of the sectorized mesh comparison.** The paper alternates between treating the sectorized mesh as a comparator (Table VIII, Fig. 8) and disclaiming the comparison due to different functional scope (Table IX, Section III-B.4). The "14× bandwidth efficiency per unit of awareness" metric (Section IV-G) is presented as a key finding but depends on the assumption that cluster-wide awareness and local-neighbor monitoring are comparable services. **Required:** Either commit to the comparison with a clear functional-equivalence argument, or remove the quantitative efficiency comparison and present the mesh only as a reference point with explicitly different capabilities.

## Minor Issues

1. **Eq. (4):** The global-state mesh message count $M_{\text{mesh}} = O(N \cdot f \cdot \log N) = O(N^2)$ uses $f = N/\log N$, but this is not standard gossip. The paper should note this is a worst-case construction, not a practical gossip protocol.

2. **Table III (Simulation Parameters):** The collision avoidance rate ($10^{-4}$/node/s) is described as "screening notifications" in footnote (a), but the message is labeled "collision avoidance msg" (128 B). Clarify whether these are screening alerts or maneuver commands.

3. **Section IV-A, RF-backup handoff:** The calculation "$51 \times 0.8 / 0.36$~s $\approx 113$~s" is unclear. Presumably 0.8 s is the serialization time for 100 B at 1 kbps, and 0.36 is Slotted ALOHA throughput, but this should be spelled out.

4. **Table V (Joint Interaction):** The "GE Only" column is identical to "No Loss" for all capacity levels. The footnote explains this (lost messages never reach the queue), but the table presentation is confusing—it appears to show that GE has zero effect, which is misleading. Consider restructuring or adding a "GE link loss rate" column.

5. **Section III-B.2:** "the coordinator detects failure within one cycle" assumes the coordinator is always available. Under the double-fault scenario (coordinator failure + optical outage), failure detection is delayed by ~160 s. This should be noted.

6. **Eq. (6):** The AoI P99 formula uses $\lceil \cdot \rceil$ (ceiling), which is correct for discrete cycles, but the derivation assumes geometric inter-report intervals without accounting for the initial report at cycle 0. Clarify the boundary condition.

7. **Abstract:** "open-source Monte Carlo tool confirms implementation consistency to <0.1%" could be misread as physical validation. Suggest: "confirms analytical-to-simulation implementation consistency to <0.1%."

8. **Section II-B:** "Bio-inspired optimization (ACO, PSO, ABC) lacks convergence guarantees at $10^6$ scale" is an overly broad claim. PSO and ACO have convergence results under specific conditions; the issue is practical scalability, not theoretical guarantees.

9. **Table II footnote (a):** States AoI is unchanged across bandwidth regimes, which is correct under the model but should note that higher bandwidth enables higher $p_{\text{exc}}$, which would reduce AoI.

10. **Formatting:** The paper uses both "msg/s" and "messages/s" inconsistently. Standardize.

## Overall Recommendation

**Major Revision**

This paper presents a useful systems engineering framework for sizing hierarchical coordination architectures in large space swarms. The three-layer feasibility decomposition, the design equations summary, and the transparent treatment of limitations are valuable contributions. However, the paper suffers from four significant weaknesses: (1) the absence of any physical-layer validation, combined with tight margins (623 ms at $\gamma = 0.85$, 98 ms at $\gamma = 0.80$) that make the TDMA feasibility claims fragile; (2) the DES-to-analytical agreement is presented as a validation result when it is actually an implementation verification; (3) the stress-case workload that drives the most dramatic results lacks operational justification; and (4) the topology comparisons mix architectures with different functional scopes in ways that could mislead. A major revision addressing these issues—particularly adding even a simplified packet-level validation of the TDMA superframe and grounding the workload profiles in operational data—would substantially strengthen the paper.

## Constructive Suggestions

1. **Add a single-cluster packet-level validation.** Even a simplified NS-3 or custom simulation of 100 nodes with TDMA slot scheduling, half-duplex switching, and realistic guard times would transform the paper. The superframe budget (Table IV) provides the specification; implementing it would take modest effort and would either confirm the analytical margins or reveal where they break down. This is the single highest-impact improvement.

2. **Ground the workload profiles in operational data.** Contact SpaceX's FCC filings, ESA's space debris office reports, or published conjunction screening statistics to estimate realistic command rates. Even order-of-magnitude estimates (e.g., "Starlink performs ~X orbit adjustments per satellite per year, implying a per-node command rate of Y") would dramatically strengthen the stress-case justification.

3. **Restructure the paper around the design equations, not the DES.** The paper's primary contribution is the closed-form sizing framework. The DES is a verification tool, not a discovery tool. Reframing the paper to lead with the analytical framework and use the DES only for tail statistics and joint interaction checks would be more honest and more impactful. This would also allow significant length reduction.

4. **Consolidate the overhead notation.** Replace the nine $\eta$ variants with a single parameterized expression $\eta(p_{\text{cmd}}, p_{\text{exc}}, \gamma)$ and present a single design chart showing the feasibility region in $(p_{\text{cmd}}, p_{\text{exc}})$ space for different $\gamma$ values. This would be more useful to practitioners than the current enumeration of special cases.

5. **Explicitly characterize the failure mode when superframe margin goes negative.** What happens at $\gamma < 0.80$? Does the system gracefully degrade (some reports missed) or catastrophically fail (queue overflow, cascading coordinator failures)? The current analysis stops at the feasibility boundary; extending it to characterize degraded-mode behavior would significantly increase practical value.