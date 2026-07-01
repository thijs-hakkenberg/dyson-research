---
paper: "02-swarm-coordination-scaling"
version: "s"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-24"
recommendation: "Major Revision"
---

# Peer Review: "Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study"

## 1. Significance & Novelty
**Rating: 3 (Adequate)**

The paper addresses a genuinely important problem: how to coordinate autonomous spacecraft at scales beyond current operational experience (>10⁴ nodes). The gap identified—the absence of systematic, byte-level traffic accounting comparisons of coordination architectures across the 10³–10⁵ range—is real and worth filling. The Age-of-Information analysis for exception-based telemetry and the coordinator bandwidth stress test are the most practically useful contributions, as they provide actionable design parameters for mega-constellation operators.

However, the novelty is substantially undermined by the central analytical observation the authors themselves acknowledge: the O(1) overhead scaling of the hierarchical architecture is a direct mathematical consequence of its O(N) message structure divided by O(N) fleet bandwidth. The DES essentially computes the same deterministic byte sums as the closed-form expression (Eq. 14), confirmed by the <0.05% agreement between DES and analytical predictions at all fleet sizes. The MC variance of SD < 0.001% further confirms that the simulation is near-deterministic. This raises a fundamental question about the value added by the simulation over back-of-envelope traffic accounting. The authors address this by claiming three DES-specific contributions (protocol coefficient quantification, queue stability confirmation, analytical cross-check), but the first is obtainable from the closed-form expression, the second is unsurprising given the low utilization levels (ρ_c = 0.05), and the third is a code validation exercise rather than a scientific finding.

The sectorized mesh comparator and the AoI analysis represent the strongest novel elements. The AoI results (P99 > 400s at p_exc = 0.10) provide a genuinely useful engineering trade-off that is not obvious from first principles. The coordinator bandwidth thresholds (50 kbps unscheduled, 24 kbps TDMA) are also practically valuable. These contributions, however, are secondary results within the paper's framing, which centers on the overhead scaling characterization.

## 2. Methodological Soundness
**Rating: 2 (Needs Improvement)**

The cycle-aggregated DES framework is clearly described and the traffic accounting is meticulous (Tables 4, 5, 6). The explicit enumeration of what is and is not modeled (Table 2) is commendable and should be standard practice. The Monte Carlo framework (30 replications, bootstrap CIs) is appropriate in principle, though the near-zero variance renders it largely ceremonial.

**The core methodological concern is circularity.** The DES implements a deterministic message model where each node generates exactly one status report per cycle, each coordinator generates exactly one summary, and each node receives exactly one command. The "simulation" therefore reduces to counting predetermined message types and multiplying by their fixed sizes—which is precisely what Eq. 14 does analytically. The authors acknowledge this (Section IV-D: "the close agreement is expected: the DES computes the same per-cycle byte sums"), but do not adequately address why a simulation was necessary. The claim that the DES confirms "queue stability" is weak: with coordinator utilization at ρ = 0.05, queue instability would require a fundamental implementation error, not a scaling phenomenon.

**The stress-case workload assumption is problematic.** The dominant term in η is the "one 512-byte coordination command per node per cycle" assumption (Section IV-D-2). The authors note this is a "conservative stress-case" and that "many coordination regimes would issue per-cluster commands or event-driven commands at lower rates." This means the headline result (η ≈ 21%) is driven by a parameter choice that the authors themselves consider unrealistic for many applications. The paper would benefit from presenting results under multiple workload models rather than a single stress case.

**The comparison architecture set is unbalanced.** The centralized baseline (c=1) is an intentional worst case, and the global-state mesh is an intentional upper bound. While the authors are transparent about this, the practical implication is that the hierarchical architecture is being compared against deliberately weak opponents. The sectorized mesh is a welcome addition but is itself a hybrid architecture with coordinator roles, making the comparison less clean than presented. A comparison against a realistic parallelized centralized system (c=100) with ISL-augmented ground links would be far more informative for practitioners.

**The Bernoulli link loss model is overly simplistic.** LEO inter-satellite links experience deterministic, geometry-driven outages (Earth occlusion, sun exclusion zones) that are correlated across multiple links simultaneously. The i.i.d. Bernoulli model cannot capture the scenario most dangerous to hierarchical coordination: simultaneous loss of multiple coordinator-to-member links within a cluster due to geometric alignment. The authors acknowledge this limitation but do not bound its potential impact.

## 3. Validity & Logic
**Rating: 3 (Adequate)**

The conclusions are generally supported by the analysis, and the authors are commendably transparent about limitations. The paper contains extensive caveats, footnotes, and qualification statements that demonstrate intellectual honesty. Several specific validity concerns merit attention:

**The 2.2× overhead ratio claim (hierarchical vs. sectorized mesh) requires careful interpretation.** The sectorized mesh is parameterized with capped fanout (≤10 heartbeat neighbors), which is a specific design choice, not an inherent property of decentralized architectures. The authors note this but the abstract and conclusion present "~2.2× higher overhead" as a general finding. A different capped fanout (e.g., 5 neighbors) would produce a different ratio. The claim should be more precisely qualified as applying to the specific parameterization tested.

**The extrapolation to 10⁶ nodes (Fig. 2) is acknowledged as analytical but may mislead readers.** The figure caption notes this, but the inclusion of an unvalidated extrapolation in a paper whose stated contribution is DES validation is incongruous. Physical-layer effects that the authors identify as potentially scale-dependent (MAC contention, correlated failures, antenna scheduling) are precisely the effects most likely to manifest at 10⁶ nodes.

**The AoI analysis is sound within its assumptions** but the Bernoulli exception model (each cycle is an independent trial) produces geometric inter-report intervals that may not reflect realistic spacecraft dynamics. A node on a predictable orbit would have long periods of no exceptions followed by bursts during maneuvers or perturbation events—a bursty process, not memoryless. The geometric distribution likely understates tail AoI during quiet periods and overstates it during active periods.

**The coordinator bandwidth analysis (Table 8) is the most convincing result** because it identifies a non-obvious engineering constraint: the gap between theoretical minimum (20.5 kbps) and practical zero-drop threshold (50 kbps) under random-phase access. This 2.5× factor is a genuine simulation finding that would not emerge from simple traffic accounting.

## 4. Clarity & Structure
**Rating: 4 (Good)**

The paper is well-organized and clearly written, with a logical progression from framework description through results to discussion. The extensive use of tables (11 tables) and figures (10 figures) supports the narrative effectively. Several structural choices deserve praise:

- Table 2 (Simulation Abstraction Scope) is an excellent practice that should be adopted more widely.
- The explicit traffic accounting (Table 5) with inclusion/exclusion flags for each message type eliminates ambiguity.
- The "Baseline Interpretation Note" (Section I-C) proactively addresses the most obvious criticism of the comparison set.

However, the paper is excessively long for its core content. At approximately 12,000 words of body text plus extensive tables and figures, it substantially exceeds typical IEEE T-AES length guidelines. Much of the length comes from defensive elaboration—explaining why the near-deterministic results are still meaningful, why the baselines are intentionally weak, why the MC variance is low, etc. While this transparency is appreciated, it suggests the authors are aware that the core contribution may not sustain a full journal paper. The paper could be shortened by 30% without losing essential content by: (a) moving the sectorized mesh details to an appendix, (b) condensing the sensitivity analysis, and (c) reducing the repetitive qualification statements.

The abstract is accurate but dense; the three key engineering results (AoI trade-off, coordinator bandwidth thresholds, retransmission envelope) are the strongest elements and should be more prominent. The notation is generally consistent, though the overloading of η (protocol overhead) and η_eff (MAC-adjusted overhead) requires careful reading.

## 5. Ethical Compliance
**Rating: 4 (Good)**

The AI-assisted methodology disclosure in the Acknowledgment section is appropriate and transparent. The authors clearly state that AI tools (Claude, Gemini, GPT) were used for "exploratory ideation" and that the resulting concepts are "not validated in the current study." This is a responsible approach to AI disclosure.

The anonymous authorship ("Project Dyson Research Team") with a promise to provide individual names for final publication is unusual but not unprecedented for IEEE submissions. The data availability statement with a GitHub repository link (pending commit hash) supports reproducibility, though the repository should be populated before acceptance.

One concern: the paper cites a companion methodology paper [dyson_multimodel] that appears to be self-published on the project website rather than peer-reviewed. This reference should be clearly marked as non-peer-reviewed, or the relevant methodological details should be incorporated into the current paper.

## 6. Scope & Referencing
**Rating: 3 (Adequate)**

The paper is appropriate for IEEE T-AES in topic, though the simulation-heavy methodology with limited physical-layer fidelity may be better suited to a systems engineering or networking venue (e.g., IEEE Systems Journal, IEEE Transactions on Network Science and Engineering). The references are generally relevant and span the appropriate literature domains (distributed systems, constellation management, swarm robotics, queueing theory).

Several referencing concerns: (1) Multiple references are non-archival (SpaceX website, Amazon website, DARPA program pages, DoD fact sheets). While understandable for current operational systems, the paper relies on these for key claims about operational scale. (2) The NRL swarm reference [nrl_swarm] is described as a "magazine article, non-peer-reviewed"—this should either be replaced with a peer-reviewed source or the claim should be qualified. (3) The paper does not cite recent work on distributed space systems coordination from the SmallSat community (e.g., Nag & Ravichandran on distributed satellite systems, or recent work on autonomous constellation management from MIT's STAR Lab). (4) The mean-field game references (Lasry & Lions, Huang et al.) are mentioned in the related work but never connected to the methodology—either develop the connection or remove the citations.

---

## Major Issues

1. **Near-tautological central result.** The headline finding (η ≈ 21%, O(1) scaling) is analytically predetermined by the message model and confirmed by the <0.05% DES-analytical agreement. The simulation adds negligible information beyond what Eq. 14 provides. The paper needs to either: (a) introduce stochastic elements that create genuine simulation-dependent behavior (e.g., dynamic cluster resizing, adaptive reporting rates, correlated failures), or (b) reframe the contribution away from overhead scaling toward the genuinely simulation-dependent results (AoI, coordinator bandwidth, retransmission robustness).

2. **Unbalanced comparison set.** Despite extensive caveats, the paper's structure invites readers to compare hierarchical coordination against a single-server centralized system and a global-state mesh—both intentionally extreme. The sectorized mesh helps but is itself a hybrid with coordinator roles. The paper should include at least one realistic centralized comparator (e.g., c=100 with 3-ground-station diversity) to demonstrate that the hierarchical architecture offers advantages over what a well-resourced operator would actually deploy.

3. **Physical-layer gap undermines engineering claims.** The coordinator bandwidth thresholds (50 kbps / 24 kbps) are presented as engineering design parameters, but they exclude link acquisition time (1–5s per new link), half-duplex turnaround, Doppler compensation, and antenna scheduling—all of which could double or triple the effective capacity requirement. Presenting these as "offered-load lower bounds" is technically correct but potentially misleading for practitioners who might use them for link budget sizing. The paper should provide explicit multiplicative correction factors (even approximate ones) for these effects.

4. **The "one command per node per cycle" workload assumption dominates the result.** The 512-byte coordination command per node per cycle accounts for 576/581 ≈ 99% of the protocol overhead (Eq. 14). This single assumption determines the headline η ≈ 21% figure. If commands are issued per-cluster (as would be typical for orbit maintenance), η drops to ~1%. The paper should present results under at least three workload scenarios (per-node commands, per-cluster commands, event-driven commands) to demonstrate the range of outcomes.

## Minor Issues

1. **Section III-F, paragraph 2**: "Note that while each regular node generates 205 bps..." — this paragraph is extremely long and covers multiple topics (coordinator bandwidth pooling, hardware implications, TDMA scheduling). It should be broken into subsections.

2. **Table 7 (Cluster Size)**: The overhead values (20.5–20.9%) vary by only 0.4 percentage points across a 10× range of cluster sizes. The table occupies significant space to convey "overhead is invariant to k_c." Consider condensing to a single sentence with the range.

3. **Eq. 6 (mesh convergence)**: The claim D = O(N^{1/3}) for a random geometric graph in 3D orbital space is stated without proof or reference. Orbital shells are approximately 2D (thin spherical shells), suggesting D = O(N^{1/2}) may be more appropriate.

4. **Section IV-C**: The duty cycle analysis (Table 8) presents specific numerical values (e.g., 95.0% handoff success at 1h, 99.5% at 24h) without explaining the underlying model. What determines handoff success probability? Is it purely the state transfer reliability, or does it include coordinator election consensus?

5. **Fig. 2 caption**: States "the $10^6$-node curve is an analytical extrapolation" but the figure is not provided for review. All figure references should be verifiable.

6. **Section III-E**: The collision avoidance rate justification (10⁻⁴/node/s = 1000× screening-to-maneuver ratio) is reasonable but the cited source [esa_space_env] reports maneuver rates, not screening rates. The 1000:1 ratio should be independently sourced.

7. **Table 1 (M/D/c sensitivity)**: The "Representative System" column labels are informal ("Single ground station thread," "Hyperscale data center"). These should reference actual system capabilities with citations.

8. **Notation inconsistency**: The paper uses both $k_c$ (cluster size) and $k_s$ (sector size) but also uses $k$ without subscript in Section III-C-3 ("$O(k)$ per round"). Clarify which $k$ is intended.

9. **Section V-A**: The claim that "Starlink's expansion to 42,000 satellites enters the regime where centralized coordination incurs significant overhead" is not supported by the paper's own analysis, which shows centralized processing is not the binding constraint (parallelization resolves it). The binding constraints (propagation latency, spectrum) apply at current scale too.

10. **References**: [dyson_multimodel] is a self-citation to a non-peer-reviewed source. IEEE policy requires that self-citations to unpublished work be minimized and clearly identified.

## Overall Recommendation

**Major Revision**

The paper addresses an important problem and demonstrates careful engineering analysis, particularly in the AoI, coordinator bandwidth, and retransmission robustness sections. However, the central contribution—overhead scaling characterization—is analytically predetermined and the simulation adds minimal information beyond the closed-form expression. The comparison architecture set, despite extensive caveats, remains unbalanced. The paper would benefit substantially from: (1) reframing around the genuinely simulation-dependent results rather than the overhead scaling, (2) adding a realistic centralized comparator, (3) presenting multiple workload scenarios, and (4) providing approximate physical-layer correction factors for the engineering design parameters. The authors' intellectual honesty and thorough documentation of limitations are commendable and suggest that a strong revised paper is achievable.

## Constructive Suggestions

1. **Reframe the paper around the three genuinely novel results**: AoI trade-off characterization, coordinator bandwidth thresholds, and retransmission robustness envelope. These are the findings that cannot be obtained from closed-form analysis and that provide actionable engineering guidance. The overhead scaling characterization should be presented as a validation exercise (confirming the analytical prediction holds in the DES) rather than the primary contribution.

2. **Add a realistic centralized comparator**: Implement an M/D/c centralized baseline with c=100 and model the propagation latency and spectrum constraints explicitly. This would allow the paper to make the physically-motivated argument for hierarchical coordination (latency and spectrum, not processing) with quantitative support rather than qualitative assertions.

3. **Present results under multiple workload models**: At minimum, show η under (a) per-node commands (current stress case), (b) per-cluster commands (typical orbit maintenance), and (c) event-driven commands (collision avoidance only). This would demonstrate the sensitivity of the headline result to the dominant assumption and provide practitioners with a range of expected overhead values.

4. **Couple AoI to a simplified conjunction detection model**: Even a toy model (e.g., linear-Gaussian state propagation with known perturbation noise, conjunction probability as a function of state age) would transform the AoI results from a generic freshness metric into a mission-relevant safety metric. This would substantially strengthen the paper's contribution to the space systems community.

5. **Reduce paper length by 25–30%**: Consolidate the defensive qualification passages (many of which repeat the same caveats in slightly different words across Sections I-C, III-F, IV-D, V-D, and VI). Move the sectorized mesh detailed traffic accounting to an appendix. The core results and their implications can be communicated more effectively in a shorter paper.