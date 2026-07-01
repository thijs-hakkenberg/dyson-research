---
paper: "02-swarm-coordination-scaling"
version: "af"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-27"
recommendation: "Major Revision"
---

# Peer Review: "Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study"

## 1. Significance & Novelty

**Rating: 3 (Adequate)**

The paper addresses a legitimate gap: systematic characterization of coordination overhead for autonomous spacecraft swarms at the 10³–10⁵ scale with byte-level traffic accounting. The motivation is timely given mega-constellation expansion plans, and the framing around a fixed 1 kbps per-node control-plane budget is a sensible engineering constraint. The four contributions—coordinator capacity sizing, AoI characterization, correlated loss analysis, and workload envelope decomposition—are individually useful design inputs for constellation architects.

However, the novelty is substantially limited by the authors' own candid admissions. The abstract states "individual metrics are analytically tractable in isolation" and the DES serves as a "validated parametric design tool." The $O(1)$ overhead scaling is described as "a direct mathematical consequence of the fixed-depth hierarchical message structure" (Section IV-E). The AoI P99 matches the geometric distribution "within one cycle." The GE retransmission result ($1 - 0.9^3 = 27.1\%$) is elementary probability. The paper is essentially a careful bookkeeping exercise confirming closed-form predictions across a parameter sweep. While there is value in such systematic integration, the intellectual contribution is modest for a top-tier transactions journal. The paper would benefit from at least one result where the DES reveals behavior not predictable from the analytical models—e.g., emergent queueing interactions, cascading coordinator failures, or nonlinear scaling transitions.

The comparison framework is also somewhat artificial. The centralized baseline uses $c=1$ (acknowledged as intentionally weak), the global-state mesh requires full fleet replication (acknowledged as an upper bound), and the sectorized mesh is a parameterized intermediate. The hierarchical architecture is thus compared against two strawmen and one parameterized variant. A more compelling comparison would pit the hierarchy against realistic alternatives: e.g., a DHT-based overlay, a geographic routing protocol, or a hybrid ground-augmented architecture.

## 2. Methodological Soundness

**Rating: 3 (Adequate)**

The cycle-aggregated DES methodology is clearly described and appropriate for the message-layer abstraction chosen. The Monte Carlo framework (30 replications, bootstrap CIs) is standard, and the authors correctly note that the near-deterministic message model renders MC variance negligible (SD < 0.001%). The validation against M/D/1 Pollaczek-Khinchine predictions (within 2%) and gossip convergence bounds is appropriate.

Several methodological concerns arise:

**The abstraction level may be too high to produce actionable results.** Table 5 (Simulation Abstraction Scope) reveals that MAC scheduling, link acquisition, pointing constraints, half-duplex turnaround, Doppler effects, priority queueing, and antenna beam scheduling are all abstracted away. The $\gamma \in [0.7, 0.9]$ MAC efficiency factor is applied as a simple multiplicative correction, but in practice these effects interact nonlinearly—especially at the coordinator ingress bottleneck where 100 nodes must share access to a single receiver. The TDMA analysis (Eq. 10) assumes perfect slot synchronization modulo a 15% guard time, but in LEO with relative velocities of ~7.5 km/s, Doppler shifts, and varying propagation delays across a cluster spanning potentially thousands of kilometers, achieving this synchronization is itself a significant engineering challenge that consumes coordination overhead not accounted for in the model.

**The coordinator bandwidth analysis conflates offered load with achievable throughput.** The 21–50 kbps coordinator ingress requirement (Section IV-A) is presented as a link capacity sizing result, but the analysis assumes all 100 members can simultaneously access the coordinator's receiver. In practice, this requires either (a) a phased-array receiver with 100 simultaneous beams, (b) TDMA with the synchronization overhead noted above, or (c) FDMA/CDMA with corresponding spectral efficiency penalties. The paper acknowledges this ("every node's transceiver must be capable of the coordinator ingest rate") but does not adequately address the physical-layer implications.

**The Gilbert-Elliott model parameters lack justification.** The GE transition probabilities ($p_{GB} = 0.05$, $p_{BG} = 0.20$ per cycle) are stated without reference to measured LEO ISL channel statistics. The steady-state availability of 80% ($\pi_G = p_{BG}/(p_{GB}+p_{BG}) = 0.8$) is reasonable for Earth-occluded links but the burst duration statistics (mean bad-state duration = 5 cycles = 50 s) should be validated against orbital geometry for specific altitude/inclination combinations.

**The collision avoidance event rate sensitivity is insufficient.** The $10^{-4}$/node/s rate is justified by a 1000:1 screening-to-maneuver ratio, but this ratio is highly dependent on orbital shell density and screening volume parameterization. At $10^5$ nodes in a single shell, the screening event rate could be orders of magnitude higher due to the $O(N^2)$ scaling of pairwise conjunctions. The linear sensitivity analysis (varying from $10^{-5}$ to $10^{-3}$) does not capture this density-dependent scaling.

## 3. Validity & Logic

**Rating: 3 (Adequate)**

The analytical cross-checks are thorough and the DES-to-analytical agreement is excellent (< 0.1% for overhead, within one cycle for AoI P99). The conclusions are generally well-supported by the data, and the authors are commendably transparent about limitations.

However, several logical issues deserve attention:

**The $O(1)$ overhead claim requires careful qualification.** The paper repeatedly emphasizes that hierarchical overhead is $O(1)$ (constant with $N$), but this is true only because the hierarchy depth is fixed at 4 levels and the cluster size $k_c$ is fixed. If $k_c$ were allowed to grow with $N$ (e.g., to reduce the number of coordinators), overhead would change. More importantly, the $O(1)$ property holds for the *ratio* $\eta$, but the *absolute* coordinator ingress requirement scales as $O(k_c)$, and the number of coordinators scales as $O(N/k_c)$. The fleet-wide coordinator infrastructure cost is therefore $O(N)$, not $O(1)$. The paper should more clearly distinguish between per-node overhead ratio (constant) and system-level infrastructure requirements (linear).

**The sectorized mesh comparison is not apples-to-apples.** The sectorized mesh includes peer heartbeats (32 B × 10 neighbors) that provide local collision screening capability not present in the hierarchical architecture. The hierarchical architecture relies entirely on the coordinator for collision awareness, creating a single point of failure for safety-critical functions. The overhead comparison ($1.35–1.95\times$) conflates the cost of providing different levels of situational awareness. A fairer comparison would equalize the collision screening capability—e.g., by adding peer-to-peer collision alerts to the hierarchical model.

**The AoI-to-position-error coupling is too speculative.** While the authors appropriately caveat this as "illustrative" and "back-of-the-envelope," the linear uncertainty growth model ($\dot{\sigma} = 0.5$ m/s) is presented with enough specificity to invite misinterpretation. Along-track uncertainty growth from drag is highly nonlinear over 440 s (7+ minutes), depends strongly on altitude, solar activity, and ballistic coefficient, and the relevant metric for conjunction screening is the 3D miss distance covariance, not 1D along-track uncertainty. The 230 m figure could be off by an order of magnitude in either direction. I would recommend either removing this coupling entirely or replacing it with a proper reference to covariance realism studies.

**Table 8 (Duty Cycle Trade-offs) lacks derivation.** The power variance, handoff success, and system availability values appear without supporting analysis. How is "power variance" defined and computed? Why does handoff success *increase* with longer duty cycles (fewer handoffs should mean fewer opportunities for failure, but each handoff transfers more state)? The 99.5% system availability at 24 h duty cycle—is this from the DES or analytical?

## 4. Clarity & Structure

**Rating: 4 (Good)**

The paper is generally well-written and logically organized. The "Roadmap" paragraph at the beginning of Section IV is helpful. The consistent use of traffic accounting tables (Tables 3, 4, 6, 7) provides excellent traceability. The design equations summary in Section V-C is a valuable practitioner reference.

Several structural issues reduce readability:

The paper is extremely long for a transactions paper. At approximately 12,000 words of body text plus extensive tables and figures, it exceeds typical IEEE T-AES length guidelines. Much of the length comes from exhaustive qualification and caveating—while intellectually honest, this creates a defensive tone that obscures the core contributions. For example, the abstract alone is ~250 words and contains seven parenthetical qualifications. The paper would benefit from moving some of the sensitivity analyses (e.g., Table 10 neighbor-cap sweep, Table 14 exception-based validation) to supplementary material.

The notation is generally consistent but has some issues. $\eta$ is used for both protocol overhead and MAC efficiency in different contexts (though $\gamma$ is used for MAC efficiency in most places, $\eta_{\text{eff}} = \eta/\gamma$ creates potential confusion). The coordinator processing rate uses $\mu_s$ (centralized), $\mu_c$ (cluster), and $\mu_r$ (regional) without a unifying notation.

Figures are referenced but provided as PDF placeholders (e.g., `fig-architecture-diagram.pdf`), making it impossible to evaluate their quality. The figure captions are detailed and informative, which partially compensates.

The "Baseline Interpretation Note" (Section I-C) is an unusual structural choice—essentially pre-emptively defending against a reviewer criticism. While the transparency is appreciated, this would read better integrated into the relevant methodology sections.

## 5. Ethical Compliance

**Rating: 4 (Good)**

The paper includes an appropriate acknowledgment of AI-assisted ideation (Claude 4.6, Gemini 3 Pro, GPT-5.2) in the Acknowledgment section, with a clear statement that the AI-generated concepts "are not validated in the current study." The reference to a companion methodology paper [dyson_multimodel] provides additional transparency. The data availability statement with a specific repository tag (`paper-02-v-af`) supports reproducibility.

Two minor concerns: (1) The author block uses "Project Dyson Research Team" with a footnote promising individual names for final publication. IEEE policy requires named authors; this should be resolved before acceptance. (2) The extent of AI assistance in writing the paper itself (as opposed to ideation) is not disclosed. Given the paper's polished prose and exhaustive qualification style, clarification would be appropriate under IEEE's AI disclosure policies.

The 2% annual failure rate assumption is attributed to Castet and Saleh [castet_smallsat_reliability], which is a 2009 paper. More recent reliability data from the large-scale Starlink constellation would strengthen this assumption, though the sensitivity to failure rate is likely minimal given the paper's focus on communication overhead.

## 6. Scope & Referencing

**Rating: 3 (Adequate)**

The paper is appropriate for IEEE T-AES in scope, addressing autonomous spacecraft coordination with quantitative engineering analysis. The reference list (48 citations) covers the relevant literature broadly, including constellation operations, swarm robotics, distributed systems theory, queueing theory, and space communication standards.

Several referencing gaps are notable:

**Missing recent work on distributed satellite systems.** The paper does not cite recent work on distributed space systems coordination, including: (a) the ESA OPS-SAT and related on-board autonomy demonstrations; (b) recent work on inter-satellite link network design for mega-constellations (e.g., Bhattacherjee et al., SIGCOMM 2019 on Starlink/Kuiper ISL topology); (c) the growing literature on space traffic management and autonomous collision avoidance (e.g., Hobbs et al., 2020); (d) recent AoI literature specific to satellite networks (e.g., satellite-IoT AoI optimization papers from 2022-2024).

**Several references are non-archival.** References [starlink_ops], [kuiper], [darpa_offset], [darpa_blackjack], [dod_replicator], and [nrl_swarm] are websites, press releases, or magazine articles. While some non-archival sources are unavoidable for operational systems, the paper relies on these for key claims about current constellation scale and military swarm demonstrations. The [dyson_multimodel] self-citation is to a URL with no publication venue.

**The DTN/BPv7 literature is underutilized.** Given that the paper's key finding on correlated losses points to inter-cycle store-and-forward as essential, the DTN literature deserves more than a single RFC citation [cerf_dtn] and a CCSDS standard [ccsds_bpv7]. Recent work on DTN routing in LEO constellations would strengthen the discussion.

## Major Issues

1. **Insufficient physical-layer grounding for the coordinator ingress bottleneck.** The 21–50 kbps coordinator capacity requirement is the paper's most actionable result, but it is presented purely at the message layer. The paper must address how 100 nodes physically share access to a single coordinator receiver. A brief analysis of TDMA slot duration, guard time from differential propagation delay across realistic cluster diameters (e.g., 1000 km), and the resulting achievable throughput would substantially strengthen this contribution. Without this, the 21–50 kbps figure cannot be used for hardware link budget sizing—the paper's stated goal.

2. **The DES adds negligible value beyond the analytical models.** The paper's central claim is that the DES serves as a "validated parametric design tool," but every headline result matches a closed-form prediction to within 1%. The MC variance is < 0.001%. The parameter sweeps produce monotonic, analytically predictable curves. The paper needs to demonstrate at least one scenario where the DES reveals behavior not captured by the analytical models—or explicitly reposition the contribution as a reference implementation and parameter-space atlas rather than a simulation study.

3. **The comparison framework needs strengthening.** The two reference baselines ($c=1$ centralized, global-state mesh) are acknowledged strawmen. The sectorized mesh provides a more realistic comparator but differs in functionality (peer collision screening). The paper should either (a) add a comparison against a realistic alternative (e.g., DHT-based overlay, geographic routing, or hybrid ground-augmented architecture), or (b) more rigorously equalize the functional capabilities across architectures before comparing overhead.

4. **Table 8 (Duty Cycle Trade-offs) is unsupported.** The values for power variance, handoff success probability, and system availability appear without derivation, DES measurement details, or analytical justification. These are presented as key design guidance (24–48 h Pareto frontier) but cannot be verified from the information provided.

## Minor Issues

1. **Eq. 4 (hierarchical messages):** Counts only uplink reporting; the text notes bidirectional traffic "approximately doubles" overhead, but the full bidirectional message count equation is never given explicitly.

2. **Section III-B-3 (Global-State Mesh):** The convergence round formula $R_{\text{conv}} = \max(\lceil\log_2 N\rceil, \lceil N/(bf)\rceil)$ conflates two different bottlenecks (epidemic spread time vs. throughput limit) without rigorous justification. The $1.4\times$ gossip redundancy factor is stated without derivation.

3. **Table 2 (Simulation Parameters):** The footnote markers are inconsistent (a, c, d—where is b?). The collision avoidance rate footnote (a) is separated from the GE model parameters by the "Link and Processing" section, making cross-referencing difficult.

4. **Section IV-A, Eq. 8 (Chernoff bound):** The bound is stated but the derivation jumps from $\alpha \approx 2.0$ at 99.9% confidence to the DES confirming zero drops at $\alpha = 2.44$ (50 kbps). The gap between the Chernoff prediction (41 kbps) and the DES zero-drop threshold (50 kbps) is not explained.

5. **Section IV-B:** The AoI sampling interval ("sampled every 100 s") introduces discretization; at $T_c = 10$ s, this means only every 10th cycle is sampled. The impact on P99 estimation should be noted.

6. **Table 12 (Link Availability):** Footnote markers (b) and (c) appear to be swapped or mislabeled. The "Offered" column header should clarify it includes retransmission overhead.

7. **Section III-E:** "Per coordination cycle ($T_c = 10$ s), each node sends: 1 status report ($r = 0.1$ msg/s × 10 s)" — this is trivially $0.1 \times 10 = 1$; the intermediate calculation is unnecessary and slightly patronizing for the T-AES audience.

8. **Typographical:** "Lluch i Cruz" in the bibliography [golkar_federated] should verify the correct Catalan name formatting.

9. **The paper references "Claude 4.6," "Gemini 3 Pro," and "GPT-5.2"** — these model versions do not exist as of my knowledge cutoff. If this is a future-dated paper, this should be clarified; if these are fictional version numbers, they should be corrected.

## Overall Recommendation

**Major Revision**

The paper addresses a relevant problem with careful engineering analysis and commendable transparency about assumptions and limitations. The traffic accounting framework, coordinator capacity sizing, and workload decomposition are useful contributions to the constellation design literature. However, the paper suffers from three fundamental weaknesses: (1) the DES adds negligible value beyond closed-form predictions, undermining the claimed contribution of a simulation study; (2) the physical-layer abstraction is too aggressive for the coordinator ingress result to be actionable; and (3) the comparison framework relies on intentionally weak baselines. A major revision should demonstrate DES value-add (e.g., through scenarios with emergent interactions), provide physical-layer grounding for the coordinator bottleneck, and either strengthen the comparison framework or reframe the contribution as a single-architecture characterization rather than a comparative study. The paper's length should also be reduced by ~25% through consolidation of sensitivity analyses into supplementary material.

## Constructive Suggestions

1. **Add a "DES value-add" experiment.** Design a scenario where analytical predictions fail—e.g., cascading coordinator failures during a solar particle event, simultaneous handoffs creating regional coordinator overload, or interaction between GE losses and exception-based telemetry where the joint distribution differs from the product of marginals. Even a negative result ("the joint distribution matches the product to within X%") would strengthen the paper by demonstrating the DES was needed to verify this.

2. **Ground the coordinator ingress with a single-cluster physical-layer vignette.** For one specific scenario (e.g., $k_c = 100$ nodes in a 500 km diameter cluster at 550 km altitude), compute: differential propagation delay across the cluster, required TDMA guard time from this geometry, Doppler spread, and resulting achievable throughput. This 1-page analysis would transform the 21–50 kbps result from a message-layer estimate to an actionable link budget input.

3. **Replace the global-state mesh with a DHT-based or geographic routing comparator.** A Chord/Kademlia-style overlay with $O(\log N)$ routing hops and $O(\log N)$ state per node would provide a much more credible decentralized alternative than the $O(N^2)$ strawman. This would also test whether the hierarchical architecture's advantage persists against a well-designed decentralized protocol.

4. **Derive Table 8 (Duty Cycle) from first principles.** Show the handoff success probability as a function of state transfer size, link BER, and transfer duration. Derive system availability from the coordinator MTTF, election time, and duty cycle using a Markov availability model. This would convert an unsupported table into a validated design tool.

5. **Shorten the paper by consolidating sensitivity analyses.** Move Tables 10 (neighbor-cap sweep), 14 (exception validation), and the continuous command-rate sweep (Fig. 9) to an online supplement. The core paper should focus on the four headline results and their cross-checks, with sensitivity details available for interested readers. Target ~20% length reduction.