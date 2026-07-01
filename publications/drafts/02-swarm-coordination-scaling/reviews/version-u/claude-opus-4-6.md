---
paper: "02-swarm-coordination-scaling"
version: "u"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-24"
recommendation: "Major Revision"
---

# Peer Review: "Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study"

## 1. Significance & Novelty

**Rating: 3 (Adequate)**

The paper addresses a relevant problem—coordination overhead scaling for large autonomous spacecraft swarms—that sits at the intersection of mega-constellation operations, distributed systems, and swarm robotics. The authors correctly identify that no prior work has combined byte-level traffic accounting with autonomous coordination at the $10^4$–$10^5$ node scale. The workload-dependent design envelope (stress-case through nominal) and the AoI-based coordination quality analysis are useful framing contributions for system architects.

However, the core novelty is limited. The $O(1)$ overhead scaling of a fixed-depth hierarchy with constant cluster size is, as the authors themselves acknowledge (Section IV-D), "a direct mathematical consequence of the hierarchical message structure—not a surprising emergent property." The DES confirms a protocol coefficient ($\eta \approx 46\%$) that matches the closed-form prediction to within 0.1%, which validates implementation correctness but does not constitute a discovery. The paper is essentially a parametric accounting exercise over a deterministic message model, dressed in the apparatus of Monte Carlo simulation. The MC variance of SD < 0.001% across 30 replications underscores that there is almost nothing stochastic to explore—the 2%/year failure rate perturbs a negligible fraction of nodes per cycle.

The AoI analysis (Section IV-E) and Gilbert-Elliott link loss comparison (Section IV-K) add genuine value, but both are relatively straightforward applications of established frameworks. The AoI results (geometric inter-report intervals producing heavy-tailed staleness) follow directly from the Bernoulli exception model without requiring simulation. The GE analysis yields the unsurprising conclusion that retransmission during correlated outage bursts is ineffective. The sectorized mesh comparator (Section III-B.4) is a welcome addition that fills the gap between the intentional upper/lower bounds, but its $1.4$–$1.5\times$ overhead ratio is specific to the capped-fanout parameterization and may not generalize.

## 2. Methodological Soundness

**Rating: 3 (Adequate)**

The simulation framework is carefully constructed at the message-passing abstraction layer, with explicit traffic accounting (Table VI), formal metric definitions (Section III-G), and full-participation enumeration. The analytical cross-check (Section IV-D.2) is a commendable validation practice. The abstraction scope table (Table III) is unusually transparent about what is and is not modeled.

The fundamental methodological concern is that the DES adds almost no information beyond the closed-form analysis. The authors report $\eta_{\text{DES}} = 46.0\%$ matching $\eta_{\text{analytic}} = 46.1\%$ to within 0.1% at all ten fleet sizes. The three claimed DES contributions—protocol coefficient quantification, queue stability confirmation, and analytical cross-check—are essentially the same finding stated three ways: the simulation correctly implements the traffic accounting formula. Queue stability is trivially guaranteed when coordinator utilization is $\rho_c = 0.05$ (Section III-B.2); no realistic perturbation would push this to instability. The claim of "queue stability confirmation across two orders of magnitude" overstates the significance of confirming that a system at 5% utilization does not overflow.

The Monte Carlo framework (30 replications, bootstrap CIs) is appropriate methodology applied to a problem that doesn't need it. The authors acknowledge this ("the MC framework serves primarily to confirm this low-variance property rather than to explore substantial stochastic uncertainty"), but this raises the question of why 30 replications were run rather than simply presenting the analytical result with model-form uncertainty bounds. The $\eta_{\text{eff}} \in [51\%, 66\%]$ band from MAC efficiency uncertainty ($\gamma \in [0.7, 0.9]$) is far more informative than the MC confidence intervals and should be the primary uncertainty characterization.

The coordinator bandwidth stress test (Section IV-G) is one of the more valuable simulation contributions, as the interaction between random-phase arrivals and finite coordinator capacity produces non-trivial drop behavior that is harder to predict analytically. However, the TDMA analysis (Section IV-I) is entirely analytical rather than simulated, despite being identified as "priority future work" for DES implementation.

The Bernoulli exception model ($p_{\text{exc}}$ as a free parameter) is a significant limitation. The authors correctly note that "determining realistic exception rates as a function of orbital perturbation models and prediction accuracy is a necessary prerequisite for engineering application," but this prerequisite is unmet. Without coupling to orbital dynamics, the exception-based telemetry results are parametric curves rather than engineering predictions.

## 3. Validity & Logic

**Rating: 4 (Good)**

The paper is notably honest about its limitations. The baseline interpretation note (Section I-C) clearly states that the centralized and mesh baselines are intentional bounds. The extensive footnotes in Tables I, IV, and V disambiguate metric definitions. The distinction between delivered and offered overhead (Table VIII) is carefully drawn. The acknowledgment that the $10^6$-node curve in Fig. 3 is an analytical extrapolation, not DES-measured, is appropriately flagged.

The logical structure of the argument is sound: define a coordination budget → enumerate message types → compute overhead analytically → confirm via DES → explore sensitivity. The conclusions are well-supported by the analysis and do not overreach. The statement that "the hierarchical $O(1)$ overhead scaling is an analytical consequence of the $O(N)$ message structure" (Section VI) is refreshingly direct.

There are some logical tensions. The paper motivates hierarchical coordination by citing propagation latency and spectrum scarcity as "fundamental constraints on centralized architectures that parallelization cannot resolve" (Section IV-A), but the DES does not model propagation latency as a binding constraint (intra-cluster propagation is ~3.3 ms, well within $T_c = 10$ s) and does not model spectrum allocation at all. The argument for hierarchical coordination thus rests partly on physical-layer considerations that the simulation abstracts away. This is not incorrect—the physical arguments are valid—but it means the DES results alone do not demonstrate the superiority of hierarchical coordination; they characterize its overhead properties conditional on the assumption that hierarchical coordination is needed.

The sectorized mesh comparison (Section IV-A, V-C) is logically sound but the $1.4$–$1.5\times$ overhead ratio deserves more scrutiny. The capped sectorized mesh designates a sector coordinator and limits heartbeats to 10 neighbors—making it architecturally very similar to the hierarchical topology with added peer heartbeats. The comparison therefore quantifies the cost of 10 peer heartbeats (320 B/node/cycle) rather than the cost of decentralization per se. A fairer comparison might vary the heartbeat fanout to find the crossover point.

## 4. Clarity & Structure

**Rating: 4 (Good)**

The paper is well-organized and clearly written for its length (~15,000 words). The progression from framework description (Section III) through results (Section IV) to discussion (Section V) is logical. Tables are numerous (12) and generally well-formatted, though the density of footnotes in some tables (e.g., Table IV has seven footnotes) impedes readability. The traffic accounting table (Table VI) and abstraction scope table (Table III) are particularly effective at establishing the simulation's scope.

The paper is excessively long for its information content. Much of the text is devoted to explaining why the results are unsurprising (e.g., the extended discussion of why $O(1)$ scaling is analytically guaranteed in Section IV-D) or to caveating the baselines (the centralized baseline is discussed at length in Sections I-C, III-B.1, and IV-A). A more concise presentation would strengthen the paper. The workload profile definitions (Section III-H) could be a table rather than an enumerated list. The coordinator bandwidth discussion spans Sections III-F, III-F.1, IV-G, and IV-I with significant redundancy.

Figures are referenced but not included (as expected for a LaTeX source review). Based on the captions, the figure set appears comprehensive: architecture diagram, overhead scaling, latency distributions, failure resilience, cluster optimization, duty cycle Pareto, scaling trajectory, message decomposition, AoI quality, sensitivity sweeps, TDMA comparison, workload comparison, and link model comparison. This is a large figure count (13+) for a journal paper and some consolidation may be warranted.

The abstract is accurate and informative, though dense. The sentence beginning "Link robustness is evaluated under both i.i.d. Bernoulli and two-state Gilbert-Elliott..." packs too much into a single clause. The keywords are appropriate.

## 5. Ethical Compliance

**Rating: 5 (Excellent)**

The paper includes an unusually transparent acknowledgment of AI-assisted methodology: "An exploratory AI-assisted ideation exercise using Claude 4.6 (Anthropic), Gemini 3 Pro (Google DeepMind), and GPT-5.2 (OpenAI)..." with a clear statement that the AI-generated concept "is not validated in the current study." The data availability statement provides a repository URL (though the commit hash is pending). The author block notes that individual names will be provided per IEEE policy. No conflicts of interest are apparent. The research involves simulation only and raises no human subjects or dual-use concerns beyond the general applicability to military swarm systems (which is openly discussed in the related work).

## 6. Scope & Referencing

**Rating: 3 (Adequate)**

The paper is appropriate for IEEE T-AES in scope, addressing autonomous spacecraft coordination with simulation-based analysis. The reference list (52 citations) is comprehensive, spanning distributed systems theory (Lynch, Lamport, Ongaro), swarm robotics (Brambilla, Dorigo, Reynolds), constellation operations (Handley, Del Portillo, Akyildiz), queueing theory (Kleinrock), and AoI (Kaul, Yates, Sun). The related work section is thorough.

However, several relevant bodies of work are underrepresented. The paper does not cite recent work on distributed space systems coordination protocols, such as the CCSDS Spacecraft Onboard Interface Services (SOIS) or the emerging standards for autonomous satellite operations. The DTN/BPv7 reference (CCSDS 734.2-B-1) is mentioned but not integrated into the analysis, despite store-and-forward being recommended as the preferred recovery strategy for correlated outages. Recent work on LEO constellation ISL network design (e.g., Bhattacherjee and Singla, 2019; Kassing et al., 2020) is absent. The mean-field game references (Lasry, Huang) are cited but never used in the analysis.

Several references are non-archival (SpaceX website, Amazon website, DARPA program pages, DoD fact sheets, NRL magazine article). While understandable for operational systems that don't publish in peer-reviewed venues, the reliance on 5+ non-archival sources weakens the scholarly foundation. The companion methodology paper [52] is self-cited but appears to be a non-peer-reviewed project publication.

---

## Major Issues

1. **The DES adds negligible information beyond closed-form analysis.** The headline result ($\eta \approx 46\%$) is analytically derivable from Eq. (12) and matches the DES to within 0.1%. The MC variance (SD < 0.001%) confirms this is a deterministic system with trivial stochastic perturbation. The paper should either (a) introduce physical-layer effects that create genuine scale-dependent nonlinearities requiring simulation, or (b) reframe the contribution as an analytical design-space characterization with DES implementation validation, reducing the simulation apparatus accordingly. As currently written, the extensive MC framework (30 replications, bootstrap CIs, 90 minutes of compute) is methodological overkill for a near-deterministic system.

2. **The stress-case workload assumption dominates all results but is unrealistic.** The $\eta \approx 46\%$ headline figure assumes one unique 512-byte command per cluster member per cycle—acknowledged as "a conservative upper bound unlikely to be sustained indefinitely." The nominal workload ($\eta \approx 5\%$) is far more representative of steady-state operations. The paper should lead with the workload envelope (Fig. 12) rather than burying it in Section IV-J, and the abstract should present the range ($5\%$–$46\%$) as the primary result rather than emphasizing the stress-case.

3. **Absence of orbital dynamics coupling undermines engineering applicability.** The exception probability $p_{\text{exc}}$ is a free parameter unconnected to spacecraft dynamics. The AoI analysis shows P99 > 400 s at $p_{\text{exc}} = 0.10$, but without knowing what $p_{\text{exc}}$ values are realistic for different orbital regimes, this is a parametric curve rather than an engineering recommendation. Similarly, the collision avoidance event rate ($10^{-4}$/node/s) is justified by a 1000:1 screening-to-maneuver ratio, but this ratio varies enormously with orbital altitude, inclination, and fleet density. The paper should either couple to a simplified orbital model or more explicitly bound the parameter ranges for specific mission scenarios.

4. **The sectorized mesh comparison is architecturally confounded.** The capped sectorized mesh uses a sector coordinator (functionally identical to a hierarchical cluster coordinator) plus 10 peer heartbeats. The $1.4\times$ overhead ratio therefore measures the cost of adding peer heartbeats to a hierarchical architecture, not the cost of decentralization. A cleaner comparison would include: (a) a purely decentralized variant with no coordinator roles, and (b) a hierarchical variant augmented with peer heartbeats for local collision screening. This would disentangle the contributions of hierarchy vs. peer awareness.

5. **The centralized baseline comparison is misleading despite extensive caveating.** Fig. 2 shows the single-server centralized baseline diverging at $10^4$ nodes, creating a visual impression of hierarchical superiority that the text repeatedly disclaims. The $M/D/c$ sensitivity (Table I) shows that processing does not bind for $c \geq 100$, and the true arguments for hierarchical coordination (propagation latency, spectrum scarcity) are not modeled. The paper should either model these physical constraints or remove the centralized processing divergence from the primary comparison figure, replacing it with a propagation-latency comparison.

---

## Minor Issues

1. **Section III-B.1, Eq. (1):** The variable $\mu_s$ is introduced as "processing capacity (messages per second)" but later used as a service rate in the $M/D/1$ formula. Clarify that $\mu_s$ is the service rate (reciprocal of deterministic service time) to avoid confusion with throughput.

2. **Table II (cluster size):** The overhead values are identical to one decimal place across all $k_c$ values (46.0% or 46.1%). Consider reporting to two decimal places to show the actual variation, or simply state that overhead is invariant to $k_c$ and omit the table in favor of a single sentence.

3. **Section III-F:** The MAC-layer utilization calculation ("$\eta_{\text{total}} / \gamma \approx 74$–$84\%$") is presented as exceeding Slotted ALOHA capacity (~36%), but Slotted ALOHA is not a realistic MAC protocol for scheduled ISL systems. This comparison adds confusion rather than insight.

4. **Section IV-C (duty cycle):** Table III reports "Handoff Success" ranging from 95.0% to 99.9%, but the mechanism driving handoff failure is not clearly explained. Is it coordinator failure during handoff, link loss during state transfer, or timeout? The 95% success rate at 1-hour duty cycles seems low for a 1–10 second transfer over a dedicated optical link.

5. **Eq. (12):** The collision avoidance term ($N \times 0.128$ B) appears to use the per-cycle expected count ($10^{-4} \times 10 = 10^{-3}$ events/node/cycle) multiplied by 128 B, yielding 0.128 B/node/cycle. This is correct but the intermediate calculation should be shown for clarity.

6. **Section III-E:** The Palm-Khintchine theorem citation to Kleinrock [27] is appropriate, but the theorem requires that no single source dominates the aggregate—worth stating explicitly given that coordinator nodes generate more traffic than regular nodes.

7. **Table VIII footnote (b):** "Protocol offered load alone; total offered (including baseline retransmission) exceeds 100%..." The baseline retransmission overhead is not quantified. Provide the total offered load figure.

8. **Section V-A:** "Starlink's expansion to 42,000 satellites enters the regime where centralized coordination incurs significant overhead"—this claim is not supported by the analysis, which shows centralized processing is adequate to $10^6$ nodes with $c = 100$ servers. The physical-layer arguments (latency, spectrum) are the relevant ones.

9. **Reference [1]:** "accessed February 2026" appears to be a future date, suggesting the manuscript was prepared with projected access dates. Verify all access dates.

10. **The acknowledgment mentions "Claude 4.6," "Gemini 3 Pro," and "GPT-5.2"**—model versions that do not exist as of mid-2025. This suggests either future-dated writing or fabricated version numbers. Clarify.

---

## Overall Recommendation

**Major Revision**

The paper addresses a relevant problem and is executed with commendable transparency about assumptions, limitations, and baseline interpretations. The traffic accounting framework, workload envelope, AoI analysis, and coordinator bandwidth characterization are useful contributions. However, the central methodological issue—that the DES adds negligible information beyond closed-form analysis for a near-deterministic message model—undermines the paper's claim to be a "simulation study." The stress-case workload assumption inflates the headline overhead figure, the centralized baseline comparison is visually misleading despite textual caveats, and the absence of orbital dynamics coupling limits engineering applicability. A major revision should: (1) reframe the contribution as a design-space characterization with the workload envelope as the primary result; (2) introduce at least one physical-layer effect (e.g., TDMA scheduling within the DES, deterministic occlusion windows) that creates genuine scale-dependent behavior requiring simulation; (3) lead with the $5\%$–$46\%$ overhead range rather than the stress-case; and (4) either model the physical constraints motivating hierarchical coordination or restructure the comparison to avoid implying processing-based superiority.

---

## Constructive Suggestions

1. **Implement TDMA scheduling within the DES** (identified as priority future work in Section VI). This would transform the coordinator bandwidth analysis from analytical projection to simulation result, introduce genuine scale-dependent behavior (slot contention, synchronization jitter), and justify the simulation methodology. Even a simplified TDMA model within a single cluster would substantially strengthen the paper.

2. **Restructure around the workload envelope.** Make Fig. 12 (workload comparison) the primary result figure. Present the $5\%$–$46\%$ range in the abstract and introduction as the design envelope, with the stress-case as an explicit upper bound. This reframing better matches the paper's actual contribution and avoids the impression that $46\%$ is the expected operating point.

3. **Couple $p_{\text{exc}}$ to a simplified orbital prediction model.** Even a first-order model (e.g., SGP4 prediction error as a function of time since last update, with a threshold defining "exception") would transform the exception-based telemetry results from parametric curves to mission-specific predictions. This would also enable the AoI analysis to produce conjunction detection probability rather than raw staleness.

4. **Add a single-cluster packet-level validation.** Simulating one cluster ($k_c = 100$ nodes) at the packet level with realistic MAC scheduling, link acquisition delays, and half-duplex constraints would validate the message-layer abstraction and quantify the $\gamma$ parameter rather than treating it as an assumed range. This need not cover the full $10^3$–$10^5$ range—a single-cluster validation would suffice.

5. **Disentangle the sectorized mesh comparison.** Implement a variant where the hierarchical architecture adds 10 peer heartbeats per node (matching the sectorized mesh's local awareness) and a variant where the sectorized mesh removes the sector coordinator role. This would cleanly separate the overhead contributions of (a) hierarchical aggregation, (b) peer heartbeats, and (c) coordinator designation, providing more actionable architectural guidance.