---
paper: "02-swarm-coordination-scaling"
version: "ab"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-26"
recommendation: "Major Revision"
---



# Peer Review: "Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study"

**Manuscript Version:** AB
**Venue:** IEEE Transactions on Aerospace and Electronic Systems

---

## 1. Significance & Novelty

**Rating: 3 (Adequate)**

The paper addresses a genuinely important problem: how to coordinate autonomous spacecraft swarms at scales (10³–10⁵) that exceed current operational experience. The authors correctly identify a gap between swarm robotics literature (tens to hundreds of agents), constellation management literature (up to ~10⁴ nodes with ground control), and the aspirational scales of future mega-constellations and space infrastructure. The framing around byte-level traffic accounting under a fixed per-node budget is a useful engineering contribution that distinguishes this work from purely theoretical scaling analyses.

However, the novelty is more limited than the paper suggests. The core analytical result—that a fixed-depth hierarchy with fixed fan-out produces O(1) overhead ratio—is a straightforward mathematical consequence of the message model (as the authors themselves acknowledge in Section IV-E). The DES essentially verifies this known property with high precision. The four "DES-unique" contributions (coordinator burstiness, AoI tracking, GE loss characterization, workload decomposition) are individually modest: the burstiness result follows from elementary queueing of synchronized sources; the AoI analysis applies a standard framework with a simple linear uncertainty growth model; the GE result (27% vs. 87.5% recovery) is predictable from the model parameters; and the workload decomposition confirms that actuation traffic dominates when actuation traffic is the dominant message class by construction. The claim in the abstract that these are "inaccessible to closed-form analysis" is overstated—each could be derived analytically with modest effort (e.g., the GE retransmission result is computed in closed form in the paper itself, Eq. 8).

The paper would benefit from a more honest positioning: this is a useful parametric design-space exploration and reference implementation, not a fundamental advance in distributed systems theory or space systems architecture. The sectorized mesh comparator (Section III-B.4) adds value as an intermediate reference point, though its parameterization (capped fanout of 10) is somewhat arbitrary.

---

## 2. Methodological Soundness

**Rating: 2 (Needs Improvement)**

The cycle-aggregated DES framework is clearly described and the parameter space is well-documented (Table III is commendably thorough). The Monte Carlo framework with 30 replications and bootstrap confidence intervals is appropriate in principle. The code availability commitment supports reproducibility.

However, several methodological concerns are significant:

**Near-zero variance undermines the simulation's value.** The authors report SD < 0.001% across 30 replications and DES-to-analytical agreement within 0.1% (Table VII). This is not a validation success—it reveals that the simulation is essentially computing a deterministic formula. The only stochastic element (2%/year node failures) perturbs a negligible fraction of nodes per cycle. When a simulation reproduces its analytical model to four decimal places, the simulation adds no information beyond the analytical model. The authors partially acknowledge this ("the MC framework serves primarily to confirm this low-variance property") but do not grapple with its implications for the paper's contribution claims. A simulation study whose primary results are analytically predictable needs to justify why the simulation was necessary.

**The message model is too stylized.** Every node generates exactly one status report per cycle; every coordinator sends exactly one command per member per cycle (stress case); message sizes are fixed constants. There is no modeling of variable-length messages, message aggregation failures, partial state updates, or adaptive reporting rates. The collision avoidance rate of 10⁻⁴/node/s is applied uniformly regardless of orbital geometry, node density, or constellation structure. This level of abstraction may be appropriate for a first-order sizing study, but the paper's claims about "byte-level traffic accounting" suggest a precision that the model does not support.

**The coordinator bandwidth analysis conflates models.** Section IV-A presents four different ingress models (deadline, leaky-bucket, TDMA, phase-staggered) that produce thresholds ranging from 21 to 50 kbps. While the comparison is useful, the paper does not clearly recommend which model is most appropriate for a given operational scenario. The 50 kbps "headline" number from the abstract corresponds to the most conservative model (random-phase deadline), which the paper then argues is an artifact of synchronized forwarding. This creates confusion about what the actual design requirement is.

**The sectorized mesh parameterization needs stronger justification.** The capped fanout of 10 (Section III-B.4) is acknowledged as a design parameter, but the sensitivity analysis (Table IV) shows that the overhead ratio changes dramatically with the cap value. The 1.4–1.5× overhead ratio relative to hierarchical is specific to cap = 10; at cap = 5, the ratio drops to ~1.35×, and at cap = 50, it rises to ~1.95×. The paper should be more explicit that the "sectorized mesh produces 1.4–1.5× higher overhead" conclusion is parameter-dependent.

---

## 3. Validity & Logic

**Rating: 3 (Adequate)**

The paper's internal logic is generally sound, and the authors are commendably transparent about the intentional nature of the reference baselines (Section I-C). The distinction between topology-invariant baseline telemetry and topology-dependent protocol overhead is clearly maintained throughout.

Several validity concerns merit attention:

**The O(1) overhead claim requires qualification.** The paper repeatedly states that hierarchical overhead is O(1) (scale-invariant), but this holds only because the hierarchy depth is fixed at 4 levels and the fan-out parameters are held constant. If the hierarchy were allowed to grow (e.g., adding levels for N > 10⁵), or if cluster sizes were adapted to fleet size, the scaling behavior would change. The paper should more clearly state that O(1) overhead is a property of the *parameterization*, not an intrinsic property of hierarchical architectures.

**The AoI-to-position-error coupling (Eq. 7) is too simplistic to support operational conclusions.** The linear model σ_pos = σ₀ + σ̇ · AoI with σ̇ = 0.5 m/s is a rough approximation that ignores the quadratic growth of along-track errors from drag uncertainty, the dependence on altitude and ballistic coefficient, and the availability of onboard propagation. The conclusion that P99 AoI of 441s "remains within acceptable margins" for conjunction screening with >1 km threshold is not well-supported—conjunction screening depends on relative position uncertainty between two objects, not absolute position uncertainty of one object. The authors acknowledge this limitation (Section V-A, item 1) but still draw operational conclusions from the simplified model.

**The centralized baseline comparison is misleading despite disclaimers.** While the authors repeatedly note that the single-server centralized model is an intentional worst-case bound, the visual comparison in Fig. 5 shows the centralized baseline diverging at ~10⁴ nodes alongside the hierarchical architecture's flat line. A reader scanning the figures would conclude that centralized coordination fails at 10⁴ nodes, which is not true for real ground systems. The M/D/c sensitivity table (Table I) partially addresses this, but the visual framing still overstates the hierarchical architecture's advantage.

**The GE loss analysis (Section IV-C) is valid but limited.** The result that intra-cycle retransmission recovers only 27% under GE losses is correct given the parameters, but the GE model parameters (p_GB = 0.05/cycle, p_BG = 0.20/cycle) are not derived from any physical link model. The steady-state availability of 80% is stated but not justified against actual LEO link statistics. The conclusion that "store-and-forward recovery is required" is reasonable but would be stronger with physically motivated channel parameters.

---

## 4. Clarity & Structure

**Rating: 4 (Good)**

The paper is well-organized and generally well-written. The roadmap at the beginning of Section IV is helpful. The extensive use of tables (particularly Tables III, V, and VI) supports reproducibility. The distinction between modeled and abstracted phenomena (Table II) is a valuable addition that more simulation papers should emulate.

The abstract is accurate and informative, though dense. The four numbered contributions in the abstract map clearly to the paper's sections. The notation is consistent throughout (η for protocol overhead, k_c for cluster size, etc.).

Several clarity issues should be addressed:

**The paper is excessively long for its content.** At approximately 12 pages of dense text plus numerous tables and figures, the paper could be shortened by 20–30% without losing substance. The repeated explanations of the same concepts (e.g., the 1 kbps budget motivation appears in at least three places; the O(1) scaling property is re-derived multiple times) add length without clarity. The sectorized mesh model description (Section III-B.4) is particularly verbose, with the capped/uncapped distinction explained three times.

**Table VII is misleading in its presentation.** The table shows η_DES = 46.0% at all fleet sizes with Δ < 0.1%, but collapses 8 intermediate rows into a single italic note. This presentation obscures the fact that the result is trivially constant—a single row with a note would suffice. The current format implies there is interesting variation to report when there is none.

**Figure references are sometimes unclear.** Several figures are referenced (e.g., Fig. 1, Fig. 2) but the manuscript is in LaTeX source form with PDF figure references. The figure captions are generally informative, but some (e.g., Fig. 5 caption mentioning a "10⁶-node curve" as "analytical extrapolation") describe content that extends beyond the validated simulation range without sufficient warning in the main text.

---

## 5. Ethical Compliance

**Rating: 4 (Good)**

The paper includes an appropriate acknowledgment of AI-assisted methodology in the Acknowledgment section, disclosing the use of Claude 4.6, Gemini 3 Pro, and GPT-5.2 for "exploratory AI-assisted ideation." The disclosure is specific about which concepts were AI-generated (the "Shepherd/Flock" hardware class design) and explicitly states this concept "is not validated in the current study." This level of transparency exceeds current norms and is commendable.

The author attribution is unusual ("Project Dyson Research Team" with a footnote promising individual names for final publication). While this is acceptable for review, IEEE policy requires named authors for publication. The data availability statement is thorough, with specific repository URLs, tags, and software versions.

One minor concern: the reference to future AI model versions (Claude 4.6, GPT-5.2) in the Acknowledgment section suggests either forward-looking speculation or that the paper was written with assistance from tools not yet publicly available at the time of review. This should be clarified.

---

## 6. Scope & Referencing

**Rating: 3 (Adequate)**

The paper is appropriate for IEEE T-AES in its focus on autonomous spacecraft coordination, though it sits at the boundary between aerospace systems and computer science/networking. The related work section (Section II) is comprehensive, covering constellation operations, swarm robotics, multi-agent theory, and military programs.

**Reference quality is mixed.** The paper cites 45 references spanning the relevant literature, but several are non-archival (SpaceX website, Amazon website, DARPA program pages, DoD fact sheets). While these are appropriate for establishing operational context, the paper relies on them for factual claims (e.g., "approximately 7,000 active satellites" from [1]) that may not be verifiable. The NRL reference [20] is explicitly noted as "non-peer-reviewed."

**Notable omissions in the related work:**
- The paper does not cite recent work on distributed space systems using software-defined networking (SDN) approaches, which are directly relevant to the coordination architecture comparison.
- Work on delay/disruption-tolerant networking (DTN) in LEO constellations beyond the foundational Cerf et al. RFC is missing—there is substantial recent literature on Bundle Protocol performance in mega-constellations.
- The consensus literature (Olfati-Saber, Ren & Beard) is cited but not connected to the hierarchical coordinator election model. How does Raft consensus scale in the space communication environment with 10s latency and intermittent links?
- Recent work on federated learning and distributed optimization for satellite constellations is not discussed, though it represents an alternative coordination paradigm.

---

## Major Issues

1. **The simulation adds negligible information beyond the analytical model.** With DES-to-analytical agreement of <0.1% and MC variance of SD < 0.001%, the simulation is computing a deterministic formula. The four "DES-unique" contributions are either analytically tractable (GE retransmission, Eq. 8) or follow from elementary queueing theory (coordinator burstiness). The paper must either (a) introduce genuinely stochastic elements that produce non-trivial simulation-only insights (e.g., adaptive message rates, correlated failures, dynamic cluster reconfiguration), or (b) reposition the contribution as an analytical design-space characterization with simulation verification, rather than claiming the DES produces results "inaccessible to closed-form analysis."

2. **The physical-layer abstraction is too aggressive for the claimed precision.** The paper reports overhead to 0.1% precision while abstracting away MAC scheduling, link acquisition, half-duplex constraints, antenna beam scheduling, and Doppler effects (Table II). The γ ∈ [0.7, 0.9] MAC efficiency range spans a 29% uncertainty band that dwarfs all other reported variations. The paper should either (a) incorporate at least a simplified MAC model to narrow this band, or (b) report all results with the γ uncertainty explicitly propagated, rather than presenting the message-layer η as the primary result and mentioning γ as a secondary correction.

3. **The AoI operational conclusions are not supported by the model fidelity.** The linear position-error growth model (Eq. 7) is insufficient to conclude that P99 AoI of 441s is "within acceptable margins" for conjunction screening. Conjunction risk depends on relative position covariance (not absolute), probability of collision (not position error alone), and screening timeline (not instantaneous AoI). Either remove the operational conclusions or couple the AoI model to a simplified conjunction assessment framework.

4. **The sectorized mesh comparison needs strengthening.** The 1.4–1.5× overhead ratio is the paper's primary architecture comparison result, but it depends critically on the arbitrary cap = 10 parameter. The paper should either (a) derive the cap value from a conjunction screening requirement (e.g., minimum number of monitored neighbors for a given miss-distance threshold), or (b) present the comparison as a parametric family rather than a single number.

---

## Minor Issues

1. **Section I-A, paragraph 2:** "proposed space infrastructure concepts...contemplate fleets of 10⁵ to 10⁶ autonomous units in the near term" — no reference supports this specific claim for "near term." The cited O'Neill (1976) and Badescu (2006) are aspirational, not near-term proposals.

2. **Eq. 4 (M_total):** This counts only uplink messages. The text notes that "the DES models the full bidirectional traffic" but the equation is presented as the hierarchical message model. Consider presenting the full bidirectional equation.

3. **Table III footnote (a):** The 10⁻⁴/node/s collision avoidance rate explanation is thorough but would be better placed in the main text rather than a footnote, given its importance to the traffic model.

4. **Section III-B.3:** The convergence time equation T_converge = D · τ_gossip (Eq. 6) uses D = O(N^{1/3}) for a "random geometric graph in three-dimensional orbital space," but LEO constellations are approximately two-dimensional (thin shells). D = O(N^{1/2}) would be more appropriate.

5. **Table VIII (cluster size):** The latency values show only two discrete levels (340 ms and 508 ms for N = 10⁴; 508 ms and 675 ms for N = 10⁵) across all cluster sizes. This suggests the latency model has very coarse granularity—the step function should be explained.

6. **Section IV-B:** "P99 along-track position uncertainty ~230 m at 0.5 m/s growth rate" — the units are inconsistent. σ̇ = 0.5 m/s is a velocity-like quantity applied to position uncertainty growth, but the actual along-track error growth from drag uncertainty is proportional to t² (not t). Clarify that this is a linearized approximation valid only for short prediction intervals.

7. **Eq. 1 (ρ = λ/μ_s):** The notation uses μ_s for service rate but the text says "we use μ_s rather than C to avoid confusion with link capacity C_node." This is helpful but should appear before the equation, not after.

8. **Section III-E, paragraph 2:** "the effective utilization η_total/γ ≈ 74–84% for γ ∈ [0.7, 0.9] exceeds the normalized throughput limit of Slotted ALOHA (1/e ≈ 36%)" — this comparison is only relevant if Slotted ALOHA were being considered as the MAC protocol. Since the paper immediately concludes TDMA is required, this comparison adds little.

9. **Data Availability:** The repository URL (github.com/projectdyson/dyson) should be verified as accessible. The tag "paper-02-v-ab" suggests version tracking but the repository's existence cannot be confirmed from the manuscript alone.

10. **Acknowledgment section:** References to "Claude 4.6," "Gemini 3 Pro," and "GPT-5.2" appear to be future/hypothetical model versions. If these are real tools used, their release dates should be noted; if speculative, this should be clarified.

---

## Overall Recommendation

**Major Revision**

The paper addresses a relevant problem and provides a well-documented parametric exploration of hierarchical coordination scaling for space swarms. The simulation framework is clearly described, the parameter space is thoroughly explored, and the code availability commitment supports reproducibility. However, the paper's central tension—between claiming DES-unique contributions and producing results that are analytically predictable to four decimal places—must be resolved. The physical-layer abstraction gap (message layer vs. MAC layer) introduces uncertainties that dwarf the reported precision. The operational conclusions drawn from the simplified AoI model are not adequately supported. A major revision should (1) honestly reposition the contribution as a parametric design-space characterization rather than a simulation study producing novel results, (2) introduce at least one genuinely stochastic or emergent phenomenon that the DES captures and analytics cannot (e.g., dynamic cluster reconfiguration under correlated failures), (3) either strengthen or remove the AoI operational conclusions, and (4) provide a physically motivated parameterization for the sectorized mesh comparison.

---

## Constructive Suggestions

1. **Add a dynamic reconfiguration scenario.** The most compelling use case for DES over analytics would be modeling cluster splits/merges, cascading coordinator failures, or adaptive reporting rates that create emergent traffic patterns. Even a single scenario where cluster boundaries shift in response to conjunction geometry would demonstrate simulation value that analytics cannot easily capture.

2. **Couple the AoI model to a simplified conjunction assessment.** Replace the linear position-error model with a Monte Carlo conjunction probability calculation (even using simplified two-body propagation). This would transform the AoI results from abstract staleness metrics into operationally meaningful miss-distance probability distributions, dramatically increasing the paper's value to the space operations community.

3. **Derive the sectorized mesh cap from conjunction screening physics.** Use the conjunction screening volume (e.g., 50 km cross-track × 100 km along-track) and expected node density at each fleet size to compute the minimum number of monitored neighbors required for a given conjunction detection probability. This would replace the arbitrary cap = 10 with a physically motivated parameter and make the 1.4–1.5× comparison more meaningful.

4. **Incorporate a simplified MAC model.** Even a basic TDMA slot allocation model (with guard times, slot synchronization uncertainty, and ramp-up overhead) would narrow the γ ∈ [0.7, 0.9] uncertainty band and provide more credible effective overhead numbers. This would also enable the coordinator bandwidth analysis to produce a single recommended threshold rather than a 21–50 kbps range.

5. **Shorten the paper by 25%.** Consolidate the repeated explanations of O(1) scaling, the 1 kbps budget motivation, and the baseline interpretation. Merge Tables VII and the exception telemetry rows into a single compact table. Move the detailed sectorized mesh sensitivity analysis (Table IV) to an appendix. The paper's impact would increase with a tighter presentation that foregrounds the four DES contributions and minimizes redundancy.