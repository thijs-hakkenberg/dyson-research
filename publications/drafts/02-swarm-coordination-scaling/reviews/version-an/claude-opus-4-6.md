---
paper: "02-swarm-coordination-scaling"
version: "an"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-27"
recommendation: "Major Revision"
---

# Peer Review: "Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study"

**Manuscript Version:** AN
**Venue:** IEEE Transactions on Aerospace and Electronic Systems

---

## 1. Significance & Novelty

**Rating: 3 (Adequate)**

The paper addresses a legitimate gap: systematic characterization of coordination overhead for autonomous spacecraft swarms at the 10³–10⁵ scale with explicit byte-level traffic accounting. The framing around RF-backup design points is well-motivated, and the identification of the 9× workload envelope (5%–46%) as being dominated by workload assumptions rather than architecture choice is a useful insight for practitioners. The coordinator capacity sizing (21–50 kbps) and the conditional independence result (Section IV-D) are potentially valuable design inputs.

However, the novelty is substantially diminished by the paper's own admissions. The $O(1)$ overhead scaling is described as "a direct mathematical consequence of the hierarchical structure" (Section IV-F), and individual metrics are "analytically tractable" with closed-form cross-checks matching to within 0.1%–1%. The simulation confirms what the equations predict, which is appropriate for a "validated design tool" contribution but limits the intellectual novelty. The paper explicitly states the simulation is "not a discovery engine" (Section I-D), which is honest but raises the question of whether the contribution meets the novelty threshold for a top-tier journal versus, say, a conference paper or technical report with accompanying open-source tool.

The comparison with baselines is problematic from a novelty standpoint. The centralized single-server ($c=1$) and global-state mesh are acknowledged as intentional bounds, not realistic architectures. The paper concedes that "a realistically provisioned centralized baseline does not diverge until $N \approx 10^6$" — well beyond the simulated range. This significantly weakens the motivation for hierarchical coordination within the studied regime, reducing the contribution to fault tolerance during ground outages and spectrum independence, which are discussed qualitatively but not rigorously quantified through simulation.

---

## 2. Methodological Soundness

**Rating: 3 (Adequate)**

The cycle-aggregated simulation framework is clearly described, and the distinction between simulated and analytical quantities (Table VI) is commendable transparency. The Monte Carlo framework (30 replications, bootstrap CIs) is appropriate, and the authors correctly note the near-deterministic nature of most metrics (SD < 0.001%). The traffic accounting (Table VII) provides a clear audit trail for overhead calculations.

**However, several methodological concerns arise:**

The term "discrete event simulation" is stretched beyond its conventional meaning. The authors acknowledge this ("not a per-packet or per-bit DES") but continue using the term throughout. What is described is more accurately a cycle-aggregated analytical model with stochastic perturbations (Bernoulli/GE loss, exponential failures). The vectorized array operations over N nodes per cycle (Section III-F) confirm this is closer to a Monte Carlo accounting model than a DES. This matters because the claimed "joint-condition verification" (Section IV-D) — the primary DES-specific contribution — tests independence of mechanisms that are *modeled* as independent by construction: GE losses occur "before messages reach the coordinator ingress queue" because the simulation implements them as separate sequential steps. The independence finding is an artifact of the simulation architecture, not an empirical discovery about the physical system. The authors partially acknowledge this ("conditional on the architecture") but should be more explicit that the simulation cannot discover cross-factor interactions it does not model.

The coordinator queueing model has an internal inconsistency. The batch-arrival model ($D[k_c]/D/1$) is described in Section III-B, but Table VI reveals that "within-cycle arrival timestamps" are analytical and "coordinator CPU queueing delay" is computed from the batch model formula, not simulated. The DES enforces only aggregate byte budgets per cycle (Model A) or token-bucket constraints (Model B). This means the 5.3% drop rate at 25 kbps (Table VIII) and the zero-drop threshold at 50 kbps are consequences of the specific ingress model chosen, not emergent simulation results. The Chernoff bound analysis (Eq. 8) is presented as a heuristic but then the DES is cited as "the authoritative answer" — yet the DES implements the same random-phase model the Chernoff bound analyzes.

The inter-cycle store-and-forward recovery analysis (Section IV-C) is explicitly labeled as "analytical extrapolation, not simulated." This is appropriate transparency, but the headline result (95% recovery within 4–7 cycles) is then presented alongside simulated results without consistent visual or textual differentiation in the abstract and conclusion.

---

## 3. Validity & Logic

**Rating: 3 (Adequate)**

The internal consistency of the paper is generally good. The analytical cross-checks (AoI geometric distribution, retransmission probability, overhead accounting) all match the simulation to high precision, which validates the implementation but also confirms the simulation adds little beyond the closed-form models for single-factor analyses.

The AoI-to-position-error coupling (Eq. 12, Section IV-B) is appropriately hedged as "order-of-magnitude" and "illustrative back-of-the-envelope," but it still occupies substantial text and may give readers false confidence. The linear model $\sigma_{\text{pos}}(t) = \sigma_0 + \dot{\sigma} \cdot \text{AoI}$ with $\dot{\sigma} = 0.5$ m/s is a rough approximation; along-track uncertainty from drag grows quadratically with time for unmodeled constant drag perturbations ($\Delta r \propto \frac{1}{2} a_{\text{drag}} t^2$ for position, though velocity uncertainty grows linearly). The 230 m figure at 441 s AoI should be treated with even more caution than stated.

The sectorized mesh comparator (Section III-B.4) is a valuable addition, but the $\sqrt{N}$ sector sizing is acknowledged as "an order-of-magnitude sizing, not a precise orbital mechanics calculation." The neighbor discovery assumption (zero bandwidth cost via global position oracle) is a significant simplification that favors the sectorized mesh; the authors note 5–15% additional overhead under rapid churn but do not incorporate this into the comparison figures.

The claim that "hierarchical overhead remains constant at $\eta \approx 46\%$ across two orders of magnitude" (Fig. 7) is mathematically guaranteed by the fixed-depth hierarchy with $O(N)$ messages and $O(N)$ bandwidth. Presenting this as a simulation "result" rather than a mathematical identity is somewhat misleading, though the authors do acknowledge this in Section IV-F.

The conclusion that the hierarchical architecture's advantage is "fault tolerance during ground outages and spectrum independence at scale" is reasonable but under-supported. The fault tolerance advantage is argued qualitatively (7–29 min/day ground outage, ~9 unhandled screening events per 15-min outage at $N = 10^5$) but not simulated. A simulation of coordination degradation during ground outages — the claimed primary advantage — would substantially strengthen the paper.

---

## 4. Clarity & Structure

**Rating: 4 (Good)**

The paper is exceptionally well-organized for its complexity. The roadmap at the beginning of Section IV, the consistent traffic accounting framework (Table VII), and the simulation resolution table (Table VI) are exemplary practices that more simulation papers should adopt. The dual-regime interpretation (Section IV-F.3) clearly explains the 1 kbps design point and its relationship to nominal optical operation.

The abstract is accurate and comprehensive, though at ~250 words it is dense. The baseline interpretation note (Section I-C) is a welcome addition that preempts misinterpretation of the reference baselines.

**Areas for improvement:**

The paper is very long for a journal article. At approximately 15,000 words of body text plus extensive tables and figures, it exceeds typical IEEE TAES limits. Much of the length comes from exhaustive qualification of every result (e.g., the AoI-to-position-error discussion spans nearly a full column of caveats). While intellectual honesty is valued, this level of hedging could be condensed. The design equations summary (Section V-C) is excellent and could serve as the primary results presentation, with supporting detail moved to appendices.

Table and figure density is high (approximately 15 tables and 12 figures). Several tables are partially redundant: Tables III, VIII, and the bandwidth breakdown in Table V all present aspects of the same overhead accounting. Consolidation would improve readability.

The notation is generally consistent, but $\eta$ is overloaded: it represents offered overhead in most tables, delivered overhead in some contexts, and effective (MAC-adjusted) overhead in others. Despite the definitions in Section III-E, this creates confusion when scanning results.

---

## 5. Ethical Compliance

**Rating: 4 (Good)**

The AI-assistance disclosure in the Acknowledgment section is transparent: Claude 4.6, Gemini 3 Pro, and GPT-5.2 are named, with a reference to a companion methodology paper. The disclosure that AI "generated several architectural concepts" but that these are "not validated in the current study" is appropriate. The data availability statement provides specific repository URLs and tags.

The anonymous authorship ("Project Dyson Research Team") with a note that "individual author names and affiliations will be provided for final publication per IEEE policy" is unusual but not unprecedented for preprints. IEEE policy requires named authors for publication; this should be resolved before acceptance.

One concern: the paper references future AI model versions (Claude 4.6, GPT-5.2) that do not exist as of mid-2025, and cites a date of "February 2026" for several web references. This suggests either the paper is set in a near-future context or the version numbers are speculative. This should be clarified — if the AI tools are hypothetical, the disclosure is misleading; if the paper is genuinely from 2026, the review timeline is unusual.

---

## 6. Scope & Referencing

**Rating: 3 (Adequate)**

The paper is appropriate for IEEE TAES in topic (space systems coordination, autonomous spacecraft). The reference list (48 items) covers the relevant literature adequately: distributed systems theory (Lynch, Lamport, Ongaro), swarm robotics (Brambilla, Dorigo), constellation management (Handley, del Portillo), queueing theory (Kleinrock), and AoI (Kaul, Yates, Kadota).

**Gaps in the literature review:**

The paper does not cite recent work on distributed space systems coordination that is directly relevant: (1) Radhakrishnan et al.'s work on networked satellite systems and inter-satellite link optimization; (2) the growing literature on federated learning for satellite constellations, which addresses similar scalability questions; (3) recent DTN performance studies for LEO mega-constellations that would contextualize the store-and-forward recovery analysis; (4) the substantial body of work on cluster-based satellite network management from the Chinese BeiDou and Hongyun constellation programs.

Several references are non-archival (DARPA program pages, Amazon marketing materials, DoD fact sheets). While these are appropriately labeled, they weaken the scholarly foundation. The companion methodology paper [42] is self-cited but appears to be a non-peer-reviewed web publication, which is problematic for a claim about AI-assisted methodology.

The paper does not engage with the operations research literature on hierarchical scheduling and resource allocation, which has directly applicable results for the coordinator capacity sizing problem (e.g., hierarchical scheduling in manufacturing systems, multi-level lot sizing).

---

## Major Issues

1. **The simulation's primary claimed contribution — joint-condition verification (Section IV-D) — is largely an artifact of the simulation architecture.** GE losses and coordinator ingress are implemented as sequential, independent processing steps. The "finding" that they compose independently is a consequence of the model structure, not an empirical result. The paper should either (a) implement a shared-medium model where the interaction could genuinely emerge and test independence there, or (b) reframe the contribution as "the simulation confirms that the point-to-point ISL model permits independent treatment of these failure modes, validating the use of separate design equations." The current framing overstates the empirical content.

2. **The hierarchical architecture's claimed advantages (fault tolerance, spectrum independence) are not quantitatively validated by the simulation.** The paper simulates overhead, latency, and loss recovery but does not simulate the ground-outage scenario that motivates the architecture. A simulation comparing hierarchical coordination continuity during a 15-minute ground outage versus centralized coordination interruption would directly support the paper's central thesis. Without this, the advantage claim rests on back-of-the-envelope calculations (Section IV-G).

3. **The near-perfect agreement between analytical predictions and simulation results (0.1% for overhead, 1 cycle for AoI) across all conditions raises the question of what the simulation adds.** The paper acknowledges this ("individual metrics are analytically tractable") but does not adequately justify why a journal-length simulation study is warranted when closed-form equations suffice. The "reproducible parametric design tool" framing is more appropriate for a software paper or technical report. For TAES, the simulation should produce at least one result that is not predictable from the analytical model — e.g., emergent behavior under combined stress conditions, or a regime where the analytical approximations break down.

4. **The $10^6$-node extrapolation in Fig. 9 and the abstract's claim about centralized divergence at $N \approx 10^6$ are not supported by simulation.** The paper simulates up to $10^5$ nodes. Extrapolation to $10^6$ assumes the fixed-depth hierarchy and message model remain valid, but at $10^6$ nodes with $k_c = 100$, there would be 10,000 cluster coordinators and 100 regional coordinators — the regional tier becomes a potential bottleneck not characterized by the current simulation. This extrapolation should be clearly labeled as analytical projection, not a simulation result, in all instances including the abstract.

---

## Minor Issues

1. **Section III-A, paragraph 1:** "We use the term 'discrete event simulation (DES)' in the sense that..." — this defensive definition suggests the authors know the usage is non-standard. Consider using "cycle-aggregated coordination model" or "message-layer simulation" consistently instead.

2. **Eq. 4 and surrounding text:** The mesh convergence formula $M_{\text{mesh}} = O(N \cdot f \cdot \log N) = O(N^2)$ requires $f = O(N/\log N)$, which is stated but the justification for why this fanout is necessary (rather than $f = O(\log N)$) could be clearer. The full-state-replication assumption drives this, but the transition from gossip protocol to information-theoretic lower bound is abrupt.

3. **Table II (M/D/c sensitivity):** The "Representative System" column labels are informal ("Single ground station thread," "Hyperscale data center"). These should either be grounded in specific system references or removed.

4. **Section IV-A, physical-layer vignette:** The cluster definition ("string of pearls" or "bounded relative-motion box") is introduced very late. This should appear in Section III (Simulation Framework) where the hierarchical topology is defined, as it affects the interpretation of all results.

5. **Table IX (coordinator bandwidth):** The column header "Msg. Delivery (%)" and footnote "c" reference is labeled "b" — there appears to be a footnote labeling error.

6. **Section IV-B, Eq. 12:** The along-track uncertainty growth rate $\dot{\sigma} = 0.5$ m/s is cited as "typical for LEO at 400–600 km" with reference to Vallado. This is a very rough number; Vallado provides propagation uncertainty models but not a single scalar rate. The citation should be more specific or the number should be presented as an assumed parameter.

7. **Fig. 9 caption:** States "the $10^6$-node curve is an *analytical extrapolation*, not DES-measured" — this critical caveat should also appear in the abstract where $10^6$ is mentioned.

8. **Section III-B.4:** "Neighbor discovery requires periodic beacons or a distributed spatial index. We assume discovery overhead is negligible because..." — this assumption favors the sectorized mesh in the comparison. The 5–15% additional overhead under rapid churn should be included as a sensitivity band in Table IV and Fig. 5.

9. **Table I (simulation parameters):** The collision avoidance rate footnote "a" explains the $10^{-4}$/node/s rate well, but the 1,000:1 screening-to-maneuver ratio should cite a specific source beyond the general ESA space environment report.

10. **Throughout:** The paper uses both "coordinator" and "cluster coordinator" interchangeably in many places. Since there are also "regional coordinators," consistent terminology would reduce ambiguity.

11. **Eq. 8 (Chernoff bound):** The notation $D_{\text{KL}}(\alpha p \| p)$ is used without defining $D_{\text{KL}}$ beyond "KL divergence." For an aerospace audience, this should be expanded.

---

## Overall Recommendation

**Major Revision**

This paper presents a carefully constructed simulation framework for hierarchical coordination overhead in large spacecraft swarms, with commendable transparency about its assumptions, limitations, and the distinction between simulated and analytical quantities. The traffic accounting methodology, design equations summary, and open-source tool contribution are valuable for the community. However, the paper's central tension — that the simulation confirms what the analytical models predict, by construction — undermines the case for a journal-length simulation study. The three major issues (artifactual independence finding, unvalidated fault-tolerance advantage, and insufficient simulation-beyond-analysis content) require substantial revision. The paper would benefit from either (a) extending the simulation to produce genuinely emergent results (ground-outage scenarios, shared-medium contention, correlated failures) that cannot be predicted from closed-form models, or (b) repositioning as a shorter paper focused on the design tool contribution with the analytical characterization as the primary content and the simulation as validation. The current hybrid — claiming simulation novelty while acknowledging analytical tractability — falls between two stools.

---

## Constructive Suggestions

1. **Simulate the ground-outage scenario directly.** Implement periodic 15-minute ground contact gaps and measure hierarchical vs. centralized coordination continuity (screening events handled, AoI degradation, command latency). This would provide the quantitative fault-tolerance comparison that is currently the paper's strongest qualitative argument but weakest quantitative evidence.

2. **Implement a shared-medium (RF bus) variant for at least one cluster** to test whether the GE/coordinator-ingress independence breaks down under contention. Even a simplified CSMA model within a single 100-node cluster would transform the independence claim from a model artifact to an empirical comparison between architectures.

3. **Shorten the paper by 30–40%** by consolidating redundant tables (merge Tables III, V, and VIII into a single comprehensive overhead accounting table), moving the physical-layer vignette and detailed Chernoff analysis to an appendix, and condensing the extensive caveats on the AoI-to-position-error coupling into a single paragraph with a forward reference to future work.

4. **Reframe the contribution around the design equations (Section V-C) as the primary output**, with the simulation serving as validation. The design equations are immediately useful to practitioners; the simulation's role as a "reproducible reference implementation" is better suited to a software/tools paper or companion technical report.

5. **Add a single "stress test" scenario where analytical predictions fail** — e.g., correlated coordinator failures (Section V-B mentions this), or a transient where 10% of clusters simultaneously re-elect coordinators. Finding the regime where the compositional design equations break down would be a genuinely novel simulation contribution and would define the tool's validity boundary.