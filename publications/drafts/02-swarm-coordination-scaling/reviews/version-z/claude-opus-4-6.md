---
paper: "02-swarm-coordination-scaling"
version: "z"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-24"
recommendation: "Major Revision"
---

# Peer Review: "Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study"

**Manuscript Version:** Z
**Venue:** IEEE Transactions on Aerospace and Electronic Systems

---

## 1. Significance & Novelty

**Rating: 3 (Adequate)**

The paper addresses a genuinely important problem: how to coordinate autonomous spacecraft swarms at scales of 10³–10⁵ nodes, a regime that is underexplored in the literature. The authors correctly identify that current constellation management (Starlink, OneWeb) relies on centralized ground control and that the scalability of autonomous in-space coordination remains an open question. The framing around a fixed 1 kbps per-node control-plane budget is a useful engineering constraint that grounds the analysis.

However, the novelty is more limited than the paper suggests. The $O(1)$ overhead scaling of the hierarchical architecture is, as the authors themselves acknowledge (Section I-D), "an analytical property of the hierarchical message structure"—it follows directly from fixed fan-out and fixed message sizes. The DES essentially confirms what the closed-form equations predict, with agreement to within 0.1% (Table VII). The three claimed DES-unique contributions—coordinator burstiness sizing, AoI characterization, and correlated loss analysis—are individually interesting but relatively straightforward applications of well-known techniques (deadline-constrained byte budgets, AoI framework from Kaul/Yates, Gilbert-Elliott channel models). None represents a methodological advance; they are parameter studies within a specific design context.

The claim in Section I-A that "no prior work has systematically compared coordination architectures for autonomous spacecraft swarms across the 10³–10⁵ range using quantitative simulation with explicit byte-level traffic accounting" is technically narrow enough to be true, but the combination of hierarchical aggregation, gossip protocols, and queueing analysis has been extensively studied in terrestrial distributed systems. The space-specific aspects (propagation delay, failure rates, optical ISL handoff) are modeled at a high level of abstraction. The paper would benefit from a more honest positioning as a parametric design-space exploration rather than implying fundamental new insights.

---

## 2. Methodological Soundness

**Rating: 2 (Needs Improvement)**

The cycle-aggregated DES framework is clearly described and the parameter space is well-documented (Table III). The Monte Carlo framework with 30 replications per configuration and bootstrap confidence intervals is appropriate in principle. However, several methodological concerns undermine confidence in the results:

**Near-zero variance undermines the simulation's value.** The authors report SD < 0.001% across 30 replications (Section III-E) and acknowledge that "the MC framework serves primarily to confirm this low-variance property rather than to explore substantial stochastic uncertainty." This is a significant red flag. If the simulation produces results indistinguishable from the closed-form equations (Table VII: agreement to 0.1%), then the DES is not providing information beyond what analytical accounting already gives. The three "DES-unique" contributions need to be examined more carefully: the coordinator burstiness result (50 kbps threshold) follows from the uniform-phase arrival model and could be derived analytically from order statistics of uniform random variables; the AoI results follow from geometric waiting time distributions under Bernoulli reporting; and the GE loss result (27% recovery) is computed directly from $1 - 0.9^3 = 0.271$. The paper needs to clearly demonstrate what the DES reveals that cannot be obtained analytically.

**The comparison architecture is structurally biased.** The centralized baseline uses $c=1$ (single server), which the authors acknowledge is an "intentional worst-case bound." The global-state mesh requires full fleet state replication, which is also an intentional upper bound. While these are labeled as reference bounds, the paper's narrative and figures (Fig. 5) still present them as comparators, creating a visual impression that the hierarchical architecture is superior when it is really being compared against strawmen. The sectorized mesh is a more meaningful comparator, but its capped-fanout variant ($\leq 10$ heartbeat neighbors) is parameterized to produce $O(N)$ scaling—the same asymptotic class as the hierarchical architecture—making the 1.4–1.5× overhead ratio a consequence of the specific byte counts chosen for heartbeats vs. commands rather than a fundamental architectural difference.

**Physical-layer abstraction is too aggressive for the claimed contributions.** The paper abstracts away MAC-layer scheduling, link acquisition, pointing constraints, half-duplex turnaround, and antenna beam scheduling (Table IV). Yet the coordinator capacity sizing result (Contribution 1) is fundamentally about intra-cycle timing—exactly the regime where MAC-layer effects matter most. The TDMA analysis (Eq. 7) assumes a guard-time fraction $\gamma = 0.85$ without justification from link-layer analysis. The claim that "deterministic scheduling (TDMA) is required" (Section III-F) is based on comparing $\eta_{\text{total}}/\gamma$ against the Slotted ALOHA limit, but the actual MAC protocol is not modeled.

**Collision avoidance rate parameterization is questionable.** The $10^{-4}$/node/s rate is justified as including screening events at a 1000:1 ratio to actual maneuvers. However, this rate produces only ~0.001 events per node per 10-second cycle, contributing negligibly to overhead (~0.1 bps per Table V). If collision avoidance is negligible in the traffic model, why is it listed as a primary event type? The sensitivity analysis (varying from $10^{-5}$ to $10^{-3}$) shows only ±1.5 percentage points of overhead change, confirming it is irrelevant to the main results.

---

## 3. Validity & Logic

**Rating: 3 (Adequate)**

The analytical framework is internally consistent, and the authors deserve credit for the careful traffic accounting (Tables II, V, VI) and the explicit separation of baseline telemetry from protocol overhead. The cross-validation between DES and closed-form predictions (Section IV-E-2, Eq. 11) is thorough.

However, several logical issues weaken the conclusions:

**The "9× design envelope" is tautological.** The three workload profiles (stress, nominal, event-driven) produce $\eta \in [5\%, 46\%]$ because they are defined to span this range. The stress case sends 512-byte commands to every node every cycle; the nominal case sends essentially nothing beyond summaries. The 9× spread is a consequence of the workload definitions, not a discovered property of the architecture. The paper acknowledges this ("dominated by workload assumptions rather than architecture choice") but still presents it as a contribution.

**The AoI results conflate two distinct phenomena.** Table VI mixes exception-based telemetry (a design choice) with link losses (an environmental constraint) in the same table. While the text distinguishes them, the presentation suggests they are comparable mechanisms. More importantly, the AoI analysis assumes that exception-based telemetry is modeled as i.i.d. Bernoulli reporting with probability $p_{\text{exc}}$, which is unrealistic—real exception-based systems report when state deviates beyond a threshold, producing temporally correlated reporting patterns that depend on orbital dynamics. The Bernoulli model produces geometric inter-report times, but actual exception-based systems would produce bursty reporting during maneuvers and silent periods during quiescent phases.

**Extrapolation beyond validated range.** Fig. 6 includes a $10^6$-node curve labeled as "analytical extrapolation, not DES-measured." While this is disclosed, the figure is titled "Message processing latency distributions at three scales," implying simulation results. The extrapolation assumes the hierarchical structure scales without encountering new bottlenecks (e.g., regional coordinator saturation, inter-cluster routing complexity), which is not validated.

The limitations section (V-C) is commendably honest about the physical-layer abstraction, priority queueing, and failure model limitations. The unresolved questions (V-B) are well-chosen and would genuinely advance the work.

---

## 4. Clarity & Structure

**Rating: 4 (Good)**

The paper is generally well-written and well-organized. The roadmap at the beginning of Section IV is helpful, and the consistent use of traffic accounting tables throughout enables the reader to verify claims independently. The separation of reference baselines from the architecture under study is clearly communicated (Section I-C).

Several structural choices merit comment:

**Positive aspects:** The abstraction scope table (Table IV) is an excellent addition that many simulation papers lack. The explicit definition of performance metrics (Section III-G) with the distinction between per-message delivery rate and per-cycle completion is valuable. The bandwidth breakdown table (Table V) provides immediate intuition about where overhead comes from.

**Areas for improvement:** The paper is quite long for a journal article (~12,000 words of body text plus extensive tables), and there is significant redundancy. The coordinator capacity discussion appears in Sections III-F, III-F-1, and IV-A with overlapping content. The overhead verification (Section IV-E) could be condensed since it primarily confirms the analytical prediction. The sectorized mesh model is introduced in Section III-B-4, discussed in Section IV-D, and revisited in Section V-A—consolidation would improve readability.

The notation is mostly consistent, though $\eta$ is overloaded: it represents protocol overhead throughout, but $\eta_{\text{total}}$, $\eta_{\text{eff}}$, $\eta_{\text{DES}}$, $\eta_{\text{analytic}}$, $\eta_S$, $\eta_N$, $\eta_E$, and $\eta_{\text{sector}}$ all appear. A notation table would help.

Figures are referenced but not provided (as expected for a LaTeX source review). The captions are descriptive and include appropriate caveats (e.g., Fig. 6's extrapolation note).

---

## 5. Ethical Compliance

**Rating: 4 (Good)**

The paper includes an appropriate disclosure of AI-assisted methodology in the Acknowledgment section, identifying specific AI systems (Claude 4.6, Gemini 3 Pro, GPT-5.2) and clarifying that the AI-generated concepts are "not validated in the current study." This is transparent and commendable. The reference to a companion methodology paper [46] provides an audit trail.

The author attribution ("Project Dyson Research Team" with a note that individual names will be provided for final publication) is unusual but acceptable for initial submission. IEEE policy requires named authors for publication, and the note indicates awareness of this requirement.

The data availability statement promises open-source code and datasets, which is excellent for reproducibility. The commit hash is marked as pending, which is acceptable at the manuscript stage.

One minor concern: the paper references AI model versions (Claude 4.6, GPT-5.2) that do not exist as of the reviewer's knowledge cutoff, and the "accessed February 2026" dates on several references suggest this manuscript may be set in a near-future context. If this is a real submission, these references need updating; if it is a speculative/pedagogical exercise, this should be disclosed.

---

## 6. Scope & Referencing

**Rating: 3 (Adequate)**

The paper is appropriate for IEEE TAES in topic (space systems coordination, autonomous spacecraft), though the contribution is more in the distributed systems/communications domain than traditional aerospace engineering. The absence of any orbital mechanics modeling beyond light-speed propagation delay means the "space" aspect is primarily contextual rather than technical.

The reference list is comprehensive (50 references) and covers the relevant literature in constellation management, swarm robotics, distributed systems, and queueing theory. Key works are cited: Lynch [7] for distributed algorithms, Kleinrock [28] for queueing theory, Demers et al. [29] for gossip protocols, and the AoI literature [48-50]. The inclusion of military swarm programs (OFFSET, Blackjack, Replicator) provides operational context.

However, several gaps exist:

- **No references to DTN simulation studies.** The paper recommends store-and-forward via DTN/BPv7 but does not cite the substantial body of DTN simulation work (e.g., Fraire et al.'s contact graph routing simulations, or the ION DTN implementation studies).
- **Missing recent mega-constellation coordination work.** The Starlink reference is a corporate website; there are peer-reviewed analyses of Starlink's autonomous collision avoidance (e.g., Muelhaupt et al., 2019, "Space traffic management in the new space era," JSSE) that would strengthen the motivation.
- **No references to hierarchical clustering in sensor networks.** The LEACH protocol (Heinzelman et al., 2000) and its descendants are directly relevant to the hierarchical coordinator rotation model and are not cited.
- **The mean-field game references** (Lasry & Lions, Huang et al.) are cited but never used in the analysis. If they are included only for completeness, they should be removed or their relevance should be made explicit.

---

## Major Issues

1. **The DES does not demonstrably produce results beyond closed-form analysis.** The headline claim is that the DES "quantifies three results inaccessible to closed-form analysis," but all three can be derived analytically: (a) the 50 kbps zero-drop threshold follows from the maximum of $k_c$ uniform random variables scaled by message size; (b) the AoI under Bernoulli exception reporting follows from geometric inter-arrival times; (c) the GE retransmission recovery rate is $1 - p_{loss,B}^{M_r+1}$. The authors must either demonstrate that the DES captures interactions or nonlinearities that the closed-form analysis misses, or reposition the paper as an analytical study with simulation verification.

2. **The comparison framework is structurally unfair.** The centralized ($c=1$) and global-state mesh baselines are acknowledged as intentional bounds, but the paper's abstract, conclusion, and figures still present them as if they demonstrate the hierarchical architecture's superiority. The sectorized mesh is the only meaningful comparator, and the 1.4–1.5× overhead ratio is driven by the specific parameterization (capped fanout = 10, heartbeat size = 32 B). A sensitivity analysis varying these parameters is needed to determine whether the ratio is robust.

3. **The physical-layer abstraction invalidates the coordinator capacity sizing claim.** The zero-drop threshold of 50 kbps (Contribution 1) is derived from a model that does not include MAC-layer scheduling, link acquisition, or half-duplex constraints. Since the contribution is specifically about intra-cycle timing and burstiness, these are exactly the effects that matter. Without at least a simplified MAC model, the 50 kbps number cannot be used for hardware sizing.

4. **The exception-based telemetry model is unrealistic.** Modeling exception reporting as i.i.d. Bernoulli with fixed probability $p_{\text{exc}}$ ignores the temporal correlation inherent in threshold-based reporting. Nodes in stable orbits would report rarely; nodes undergoing maneuvers or experiencing perturbations would report frequently. This correlation would significantly affect both AoI distributions and coordinator burstiness patterns.

---

## Minor Issues

1. **Section I-A, line "Message processing latency, bandwidth allocation..."**: The claim that these "exhibit nonlinear scaling behaviors" is not supported by the paper's own results, which show $O(1)$ overhead scaling (linear total traffic with linear total bandwidth).

2. **Eq. 4 (hierarchical messages)**: This counts only uplink messages. The text notes that "the DES models the full bidirectional traffic," but the equation should either be expanded or clearly labeled as uplink-only.

3. **Table I ($M/D/c$ sensitivity)**: The "Representative System" column labels are misleading. A "single ground station thread" processing 1,000 msg/s is not a realistic worst case; modern systems process millions of messages per second per thread.

4. **Section III-B-3**: The convergence formula $R_{\text{conv}} = \max(\lceil\log_2 N\rceil, \lceil N/(bf)\rceil)$ conflates two different bottlenecks (epidemic spread time vs. throughput-limited delivery) without formal justification. The interaction between these regimes deserves more careful treatment.

5. **Table VIII (cluster size)**: The latency values show only two discrete levels (340 ms and 508 ms for $N = 10^4$; 508 ms and 675 ms for $N = 10^5$), suggesting quantization artifacts in the simulation. This should be explained.

6. **Section IV-C**: The GE model parameters ($p_{loss,G} = 0.01$, $p_{loss,B} = 0.90$) are not justified from empirical LEO link data. The transition rate (once per $T_c = 10$ s) is also unjustified—Earth occlusion periods are typically 30–40 minutes in LEO, not 10 seconds.

7. **Eq. 11 (analytical cross-check)**: The term $N(0.128)$ appears to represent collision avoidance traffic but is dimensionally inconsistent (should be bytes, not a bare number). Clarify units.

8. **Table IX (duty cycle)**: "Handoff Success" of 95% at 1-hour duty cycle implies 5% failure rate per handoff. With ~1,000 clusters and 24 handoffs/day, this means ~1,200 failed handoffs per day. The implications for system availability are not discussed.

9. **Acknowledgment section**: References to "Claude 4.6," "Gemini 3 Pro," and "GPT-5.2" appear to be fictitious model versions. If these are real, provide version documentation; if speculative, this must be disclosed.

10. **Data availability**: The GitHub URL and commit hash are marked as pending. For review purposes, the simulation code should be available to reviewers.

---

## Overall Recommendation

**Major Revision**

The paper addresses a relevant problem and demonstrates careful engineering analysis with thorough traffic accounting and parameter documentation. However, the central claim—that the DES provides results "inaccessible to closed-form analysis"—is not convincingly supported, as all three headline contributions can be derived analytically. The comparison framework relies on intentionally weak baselines, and the physical-layer abstraction is too aggressive for the coordinator capacity sizing claim. A major revision should: (1) clearly demonstrate DES-unique insights that cannot be obtained analytically, or reposition as an analytical study; (2) strengthen the sectorized mesh comparison with sensitivity analysis; (3) add at least a simplified MAC model to ground the coordinator capacity results; and (4) replace the Bernoulli exception-reporting model with a threshold-based model that captures temporal correlation.

---

## Constructive Suggestions

1. **Demonstrate DES-unique value through interaction effects.** Run scenarios where multiple phenomena interact simultaneously—e.g., coordinator failure during a high-AoI period under GE link losses with exception-based telemetry active. If the DES captures emergent behaviors (e.g., cascading coordinator failures, AoI spikes propagating across clusters) that the closed-form analysis cannot predict, these become the genuine contributions. The current three contributions are analytically tractable in isolation.

2. **Implement a simplified MAC model for the coordinator ingress link.** Even a basic slotted ALOHA or reservation-ALOHA model within the cluster would ground the 50 kbps threshold in something more realistic than a uniform-phase byte budget. This would also enable the TDMA comparison to be a simulation result rather than an analytical overlay.

3. **Replace Bernoulli exception reporting with a state-deviation threshold model.** Define a threshold on position/velocity prediction error (e.g., report when along-track error exceeds 100 m based on a simple $J_2$ propagator). This would produce realistic temporal correlation in reporting patterns and make the AoI results operationally meaningful. It would also create genuine interaction between orbital dynamics and communication overhead that the DES is uniquely positioned to capture.

4. **Conduct a sensitivity analysis on the sectorized mesh parameterization.** Vary the heartbeat fanout cap (currently 10), heartbeat size (currently 32 B), and inter-sector relay frequency to determine whether the 1.4–1.5× overhead ratio is robust or an artifact of the specific parameter choices. If the ratio is sensitive to these parameters, the architectural comparison claim must be qualified.

5. **Reduce paper length by 20–25%.** Consolidate the coordinator capacity discussion (currently spread across three sections), merge the overhead verification subsections, and move the detailed mesh traffic accounting (Table II) to an appendix. The paper's core message—three DES-derived design parameters plus a workload envelope—can be communicated more concisely.