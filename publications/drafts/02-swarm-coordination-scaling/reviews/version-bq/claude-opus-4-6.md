---
paper: "02-swarm-coordination-scaling"
version: "bq"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-27"
recommendation: "Major Revision"
---

# Peer Review: "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms"

**Manuscript Version:** BQ
**Venue:** IEEE Transactions on Aerospace and Electronic Systems

---

## 1. Significance & Novelty

**Rating: 3 (Adequate)**

The paper addresses a genuine gap at the intersection of mega-constellation operations and autonomous swarm coordination. The claim that no prior work provides closed-form parametric sizing relationships for coordination architectures across 10³–10⁵ nodes with byte-level traffic accounting is largely credible—the LEACH literature and constellation management literature do not typically provide this level of message-layer accounting at these scales. The three-layer feasibility framework (byte budget, MAC efficiency, TDMA airtime) is a useful conceptual contribution that practitioners could apply.

However, the novelty is tempered by the nature of the results. The core finding—that architecture-specific overhead (η₀ ≈ 5%) is small while command traffic dominates—is, upon reflection, somewhat predictable from first principles. The design equations themselves (Eqs. 5, 6, 7) are straightforward accounting identities rather than deep analytical results. The AoI P99 expression (Eq. 6) is a direct application of the geometric distribution quantile; the GE recovery analysis is a standard Markov chain calculation. The paper's value lies more in the systematic assembly and cross-checking of these relationships than in any individual analytical contribution.

The paper would benefit from a stronger articulation of what *decisions* these design equations enable that were previously impossible. The abstract and introduction claim parametric sizing, but the practical design guidance is somewhat thin—the main actionable conclusion appears to be "use 24–30 kbps coordinator PHY with k_c = 100 and TDMA," which is a narrow design point rather than a broad parametric framework. The bandwidth scaling table (Table I) effectively shows that at ≥10 kbps, everything becomes trivial, which undermines the urgency of the 1 kbps analysis.

## 2. Methodological Soundness

**Rating: 3 (Adequate)**

The methodology has a fundamental structural issue: the DES and the closed-form equations operate at the same abstraction level, so the <0.1% agreement (Table VII) is essentially a code verification exercise, not validation. The authors acknowledge this explicitly (Section V-A), which is commendable, but it means the paper's empirical contribution is limited to confirming that the simulation correctly implements the analytical model. The inter-cycle GE recovery statistics (Fig. 5) represent the DES's most independent contribution, and even there the Markov chain prediction is straightforward to derive.

The cycle-aggregated DES design choice—advancing in T_c = 10 s increments with fluid-server ingress—is a significant simplification. The paper acknowledges that TDMA slot scheduling and half-duplex partitioning are checked analytically rather than simulated (noted in Section IV-D), but this means the most operationally critical constraint (the 623 ms superframe margin from Table V) has never been tested under realistic conditions. The fluid-server model cannot capture slot-level contention, guard-time violations, or the interaction between GE losses and TDMA frame timing that the authors themselves identify as important (text following Eqs. 9–10: "TDMA frame schedule is *not* decoupled from loss").

The Monte Carlo configuration (30 replications) is adequate for mean estimation given the low variance (SD < 0.001%), but the tail statistics (P99 AoI, P95 GE recovery) deserve more scrutiny. The P99 is computed per-run over ~3.15 × 10⁶ samples and then averaged across 30 runs—this is a reasonable approach, but the bootstrap CI of [438, 444] s for a quantity with an exact analytical value of 440 s primarily confirms the geometric distribution, not any emergent system behavior.

The Gilbert-Elliott model with per-cycle state transitions (coherence time = T_c) is a reasonable conservative choice, but the physical mapping (Section IV-C) reveals that the most relevant obstruction mechanism—Earth occultation at ~35 min—is explicitly excluded from the GE model and handled deterministically. This leaves structural shadowing (1–10 s) and antenna mispointing (10–60 s) as the GE targets, but the per-cycle transition model may not capture the dynamics of either well. The sensitivity sweep over p_BG partially addresses this.

## 3. Validity & Logic

**Rating: 3 (Adequate)**

The internal logic is generally sound, and the authors are commendably transparent about limitations. The three-layer feasibility framework is logically coherent, and the distinction between byte budget, MAC efficiency, and airtime scheduling is well-motivated. The decomposition of η into architecture-specific (η₀) and workload-dependent (η_cmd) components is clean and useful.

Several logical concerns merit attention:

**Coordinator failure analysis.** The triple-fault probability calculation (Section III-B, "coordinator failure + optical outage + GE bad-state: probability 0.02 × 0.01 × 0.09 = 1.8 × 10⁻⁵/yr per cluster") assumes independence of these events, but the text immediately notes they "may be correlated if the failure mode is power-negative or tumbling." This contradiction weakens the quantitative claim. The 0.01 probability for optical outage is not derived or justified.

**Sectorized mesh comparison.** The paper correctly notes the different functional scope (Table IX), but the "14× bandwidth efficiency per peer" comparison (Section IV-G) is misleading because it normalizes by a quantity (peers monitored) that the two architectures define differently. The hierarchical coordinator has full cluster state; the mesh node has partial neighbor state. These are qualitatively different information products, and normalizing them to a per-peer cost obscures this.

**The 1 kbps design point.** The justification for focusing on 1 kbps (Section III-E) is that it represents the RF-backup regime during optical outages (<1% of operational time). This is reasonable for survivability analysis, but the paper then presents most results at this operating point without consistently flagging that this is a degraded-mode analysis. The stress-case at 1 kbps (η_S ≈ 46%) combined with the 22-cycle unicast stagger represents a scenario that is simultaneously rare (optical outage) and extreme (fleet-wide reconfiguration)—the probability of needing per-node unicast commands during an optical outage should be discussed.

**Table VI (Joint Interaction).** The identical "No Loss" and "GE Only" drop columns are presented as evidence of pipeline decoupling, but this is a direct consequence of the fluid-server model: lost messages never enter the queue. Under TDMA (which the authors note is the actual operating regime), corrupted packets consume slot time, so this decoupling would not hold. The table therefore validates a model property, not a system property.

## 4. Clarity & Structure

**Rating: 4 (Good)**

The paper is well-organized and generally well-written. The roadmap at the beginning of Section IV is helpful. The notation table (Table I) is clear, and the consistent use of η₀, η_cmd, η, and η_total throughout avoids ambiguity. The explicit labeling of reference baselines vs. the architecture under study (Table VIII) is good practice.

The paper is, however, quite long and dense for the analytical depth it provides. Much of the length comes from exhaustive qualification of every result (e.g., the extensive footnotes in Tables V, VII, VIII), which, while thorough, makes the paper difficult to read in a single pass. The command dissemination model (Type 1 vs. Type 2) is introduced in Section IV-A but is critical context for the workload profiles in Section IV-E—consider introducing this taxonomy earlier.

The figures are referenced but not provided (understandable for a LaTeX source review). Based on the captions, they appear well-designed and informative. Figure 5 (cross-cycle recovery) with both DES bars and analytical curves is the strongest visualization described.

One structural issue: the Design Equations Summary (Section V-C) is buried in the Discussion. Given that the paper's stated contribution is "closed-form sizing equations," these should be more prominent—perhaps a dedicated section or a summary table with all equations collected.

The abstract is accurate but dense. The sentence "Architecture-specific overhead (heartbeats, summaries, election) is η₀ ≈ 5% of the per-node bandwidth budget—this is the topology-dependent cost" is the key finding and should appear earlier.

## 5. Ethical Compliance

**Rating: 4 (Good)**

The AI-assistance disclosure in the Acknowledgment section is appreciated and appropriately scoped ("motivated aspects of the coordinator architecture but is not validated here"). The specific models are named (Claude 4.6, Gemini 3 Pro, GPT-5.2), which is good practice. The reference to a methodology paper [dyson_multimodel] provides traceability.

The anonymous authorship ("Project Dyson Research Team") with a note about final publication is acceptable for review but must be resolved before publication per IEEE policy. The data availability statement with a specific repository tag is excellent.

One minor concern: the future model versions cited (Claude 4.6, GPT-5.2) do not exist as of my knowledge cutoff, suggesting either a speculative timeline or a different versioning convention. This should be clarified.

## 6. Scope & Referencing

**Rating: 3 (Adequate)**

The paper is appropriate for IEEE T-AES in scope, addressing autonomous spacecraft coordination at scale. The reference list is comprehensive (50+ references) and covers the relevant domains: constellation management, swarm robotics, distributed systems, queueing theory, and AoI.

However, several important gaps exist:

- **No references to actual ISL link budgets or RF system designs** for LEO constellations. The 1 kbps and 24 kbps figures are asserted without reference to any specific radio system. CCSDS Proximity-1 [ccsds_prox1] is cited for turnaround time but not for achievable data rates at the relevant link distances.

- **Missing references on cluster-based satellite network architectures.** There is relevant work on virtual satellite clustering (e.g., Radhakrishnan et al., "Survey of Inter-Satellite Communication for Small Satellite Systems," IEEE Commun. Surveys Tuts., 2016) that should be cited.

- **The LEACH comparison** (Section II-B) is appropriate but could be deeper. LEACH-C, TEEN, and other cluster-head protocols have been analyzed for overhead scaling—direct comparison of their overhead expressions with the paper's η₀ would strengthen the contribution.

- Several references are non-archival (Amazon Kuiper overview, DARPA program pages, DoD fact sheets). While understandable for operational programs, the paper relies on these for establishing the scale of the problem. At least 5 of the 50+ references are non-archival web pages.

- Reference [esa_space_env] is cited in the bibliography but I cannot find where it is cited in the text.

---

## Major Issues

1. **Validation gap undermines the contribution claim.** The paper's central claim is "closed-form sizing equations," but these equations are verified only against a simulation that implements the same equations. No physical-layer validation, no comparison with real constellation telemetry data, and no packet-level simulation exists. The authors acknowledge this, but the gap is severe enough that the paper reads as a modeling exercise rather than a validated design tool. The recommended NS-3 simulation (Section V-A) should ideally be included, at least for a single cluster, before publication in T-AES.

2. **The DES does not simulate the binding constraint.** The most critical result—the 623 ms superframe margin (Table V)—comes from analytical calculation, not simulation. The DES uses fluid-server ingress and does not enforce TDMA slot scheduling or half-duplex partitioning. Yet the paper's practical recommendation (24–30 kbps coordinator PHY) depends entirely on this analytical TDMA model. The interaction between GE losses and TDMA frame timing (acknowledged as not decoupled) is never quantified.

3. **Stress-case scenario plausibility.** The stress-case (η_S ≈ 46%) assumes every node receives a 512 B command every 10 s cycle. This is presented as "fleet-wide reconfiguration" but is not justified against any operational scenario. How long would such a campaign last? How often does it occur? The 22-cycle unicast stagger at 1 kbps means individual commands take 220 s to distribute—is this operationally acceptable for orbit-raising? Without operational context, the stress-case appears to be an arbitrary upper bound rather than a meaningful design driver.

4. **Sectorized mesh comparison is structurally unfair.** The capped sectorized mesh (cap = 10) monitors only 3.2% of sector peers, while the hierarchy provides 100% cluster coverage. Comparing their overhead values directly (65% vs. 46%) conflates architectures with fundamentally different service levels. The "14× bandwidth efficiency per peer" metric (Section IV-G) amplifies this unfairness. Either the mesh should be configured to provide comparable awareness (which would exceed the budget), or the comparison should be framed purely as "what does each architecture provide for its overhead cost" without implying one is superior.

---

## Minor Issues

1. **Eq. 2 (M/D/1 waiting time):** The formula $W_q = \rho / (2\mu_s(1-\rho))$ is the standard M/D/1 result, but the text says "mean waiting time in queue (not including service)"—this should be verified against Kleinrock's formulation, which gives $W_q = \rho / (2\mu_s(1-\rho))$ for the waiting time excluding service. Correct, but worth a brief derivation note.

2. **Section III-B, coordinator failure transient:** The RF-backup election time calculation "51 × 0.8 / 0.36 s ≈ 113 s" is unclear. If each RequestVote is 100 B = 800 bits at 1 kbps, transmission time is 0.8 s per message. With Slotted ALOHA throughput γ ≈ 0.36, the effective time per successful transmission is 0.8/0.36 ≈ 2.2 s. For 51 responses: 51 × 2.2 ≈ 112 s. But this assumes sequential transmissions—in practice, multiple responders would contend simultaneously, and the Slotted ALOHA throughput model assumes a large population. With only 51 contenders, the actual throughput may differ. This deserves clarification.

3. **Table III (Simulation Parameters):** The collision avoidance rate of 10⁻⁴/node/s seems high for screening notifications. At N = 10⁵, this yields 10 alerts/s fleet-wide, or ~100 per cycle. ESA reports ~100 actionable conjunctions per year for the entire catalog. The footnote says "screening notifications... not autonomous maneuver commands," but the rate still seems 3–4 orders of magnitude too high.

4. **Section III-D (Sectorized Mesh):** The claim that "a conjunction screening volume contains O(√N) nodes when the screening radius scales with mean nearest-neighbor distance" is stated as an "order-of-magnitude heuristic" but is not derived. For a uniform distribution on a sphere, the nearest-neighbor distance scales as N⁻¹/² (surface density), and the number of nodes within a fixed screening radius scales as N—not √N. The √N scaling requires the screening radius to shrink with N, which contradicts physical conjunction screening practice.

5. **Notation inconsistency:** p_link appears in Table IV but is not defined in Table I. The relationship between p_link and the GE model parameters (p_G, p_B, π_G, π_B) should be clarified.

6. **Section IV-A:** "Model A (hard deadline): ... C_A ≈ 50 kbps (Monte Carlo estimate from 10⁵ random arrival patterns)." This Monte Carlo estimate is not reproducible from the paper—the arrival model, drop criterion, and estimation procedure should be specified more precisely.

7. **Table V footnote:** "Under degraded γ = 0.80: slot duration grows to 98.0 ms, ingress to 9,702 ms, margin shrinks to 98 ms." This 98 ms margin is extremely tight and would likely be consumed by any unmodeled overhead. This deserves more prominent discussion rather than a table footnote.

8. **Reference [esa_space_env]** appears in the bibliography but is not cited in the text body.

9. **Acknowledgment:** "Claude 4.6, Gemini 3 Pro, GPT-5.2"—these version numbers do not correspond to any publicly released models. Clarify whether these are internal designations or speculative.

10. **Eq. 4 (mesh messages):** The notation $f = N / \log N$ is used, but the text later says $f = 17$ (for $N = 10^5$, $\log_2(10^5) \approx 17$). The base of the logarithm should be specified consistently.

---

## Overall Recommendation

**Major Revision**

The paper addresses a relevant problem and provides a systematic, well-documented message-layer analysis of hierarchical coordination overhead. The three-layer feasibility framework, the design equations, and the GE recovery characterization are useful contributions. However, the lack of any physical-layer validation—even at the single-cluster level—significantly limits the paper's practical applicability. The DES verifies the analytical model but does not validate it against any higher-fidelity representation. The 623 ms superframe margin, which is the paper's most operationally critical finding, has never been tested under realistic TDMA conditions. The sectorized mesh comparison needs restructuring to account for the different service levels. The stress-case scenario needs operational justification. A major revision incorporating at least a single-cluster packet-level simulation (as the authors themselves recommend) would substantially strengthen the contribution and make it appropriate for T-AES.

---

## Constructive Suggestions

1. **Add a single-cluster NS-3 (or equivalent) packet-level simulation.** Even a simplified model with k_c = 100 nodes, TDMA slot scheduling, half-duplex partitioning, and GE channel would validate the superframe budget (Table V) and quantify the interaction between slot-level contention and correlated loss. This is the single highest-impact addition and would transform the paper from a modeling exercise into a validated design tool.

2. **Restructure the topology comparison around functional equivalence.** Instead of comparing raw overhead numbers between architectures with different service levels, define a common service requirement (e.g., "monitor N_aware peers with AoI ≤ X") and compare the overhead each architecture requires to meet it. This would make the hierarchical vs. sectorized mesh comparison fair and informative.

3. **Provide operational scenario grounding for the workload profiles.** Map the nominal/event/stress profiles to specific operational phases (e.g., "orbit-raising campaign: 2 weeks of stress-case; routine station-keeping: event-driven; safe-mode: nominal"). Estimate the fraction of operational lifetime in each profile. This would allow readers to compute a weighted-average overhead and assess whether the stress-case is a meaningful design driver or an extreme corner case.

4. **Promote the Design Equations Summary to a standalone section** (currently buried in Section V-C). Present all equations in a single table with input parameters, output metrics, valid ranges, and sensitivity coefficients. This would make the paper's primary deliverable—the sizing equations—immediately accessible to practitioners.

5. **Quantify the γ uncertainty more rigorously.** The paper uses γ = 0.85 as a conservative estimate but derives γ = 0.949 from the slot structure. The gap between these values (accounting for FEC, ranging, control-channel overhead) is asserted but not derived. A bottom-up γ budget—analogous to a link budget—would strengthen the TDMA analysis and make the 623 ms margin claim more credible.