---
paper: "02-swarm-coordination-scaling"
version: "y"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-24"
recommendation: "Major Revision"
---

# Peer Review: "Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study"

## IEEE Transactions on Aerospace and Electronic Systems

---

## 1. Significance & Novelty

**Rating: 3 (Adequate)**

The paper addresses a legitimate gap at the intersection of mega-constellation operations and swarm coordination: the systematic characterization of hierarchical coordination overhead across the 10³–10⁵ node range with explicit byte-level traffic accounting. The authors correctly identify that swarm robotics literature rarely exceeds ~100 agents, constellation management literature rarely addresses autonomous (non-ground-directed) coordination, and networking literature does not perform byte-level overhead accounting under fixed per-node budgets. This intersection is genuinely underexplored.

However, the novelty is substantially weakened by the authors' own transparency about the nature of their results. The $O(1)$ overhead scaling—the headline finding—is acknowledged as "a direct mathematical consequence of the hierarchical message structure—not a surprising emergent property" (Section IV-D). The DES verifies this analytical property to within 0.1%, with MC variance of SD < 0.001%. This raises a fundamental question: what does the simulation contribute beyond what closed-form analysis already provides? The authors address this by identifying three DES-unique contributions (coordinator capacity sizing, AoI tracking, correlated loss characterization), which are genuinely useful engineering results. The coordinator bandwidth finding (50 kbps unscheduled vs. 24 kbps TDMA) and the Gilbert-Elliott retransmission ineffectiveness (27% vs. 87.5% recovery) are the most novel and practically useful results. The AoI analysis, while competently executed, applies a well-established framework (Kaul, Yates, Kadota) to a straightforward geometric inter-report model.

The three workload profiles producing a 9× spread in overhead ($\eta \in [5\%, 46\%]$) is a useful framing for system designers, but the insight that "control-plane sizing is dominated by workload assumptions, not architecture choice" somewhat undermines the paper's own architectural comparison. Overall, the contribution is real but incremental—it is a careful parametric characterization rather than a fundamental advance.

---

## 2. Methodological Soundness

**Rating: 3 (Adequate)**

The cycle-aggregated DES methodology is clearly described and appropriate for the message-passing abstraction layer the authors target. The decision to operate at message-layer granularity rather than packet-level is well-justified by the computational efficiency it enables (0.07 ms per node per run), and the authors are commendably transparent about what this abstraction includes and excludes (Table VI). The Monte Carlo framework (30 replications, seeds 42–71, bootstrap CIs) is standard and correctly implemented.

However, several methodological concerns arise:

**Near-tautological validation.** The DES-to-analytical cross-check (Section IV-D-2, Eq. 13) achieves <0.1% agreement because, as the authors acknowledge, "the DES computes the same per-cycle byte sums as Eq. 13, with near-zero stochastic perturbation." This is not independent validation—it is a code correctness check. The M/D/1 validation against Pollaczek-Khinchine (Section III-A) at N=100 is a genuine but limited validation. The gossip convergence validation against analytical bounds for N ≤ 1,000 is similarly limited. No validation against a higher-fidelity simulator (NS-3, OMNeT++) or operational data is provided. The authors identify packet-level validation as future work (Section V-B), but its absence is a significant gap for a paper claiming to provide "actionable design parameters."

**Coordinator queueing model.** The coordinator ingress model (Section IV-G) uses a strict per-cycle byte cap with tail-dropping, which the authors acknowledge is conservative. The alternative leaky-bucket model is mentioned but not evaluated. More importantly, the 508 ms mean latency at N=10⁵ (Table III) is dominated by regional coordinator burst arrivals (~500 ms), which is an artifact of the synchronized cycle-aggregated reporting model. The authors note that phase-offset reporting would reduce this but do not model it—yet this is arguably the most important latency-reduction lever and should be characterized.

**Sectorized mesh parameterization.** The capped-fanout sectorized mesh (Section III-B-4) caps heartbeats at 10 neighbors regardless of sector size, which is a strong assumption that drives the $O(N)$ scaling. The uncapped variant ($O(N^{3/2})$) is described analytically but not simulated. Since the capped variant is the primary comparator, the choice of cap=10 should be justified against operational requirements (e.g., how many neighbors are needed for reliable conjunction screening?).

**Statistical reporting.** The MC variance (SD < 0.001%) confirms the model is essentially deterministic for overhead metrics, making the 30-replication framework somewhat performative. The authors acknowledge this ("the MC framework serves primarily to confirm this low-variance property") but could have allocated computational effort to sensitivity analyses that would have been more informative—e.g., sweeping regional coordinator parameters ($n_r$, $\mu_r$), which are identified as "first-order design variables" but deferred.

---

## 3. Validity & Logic

**Rating: 4 (Good)**

The paper's logical structure is generally sound, and the authors demonstrate commendable intellectual honesty in qualifying their claims. The baseline interpretation note (Section I-C) is exemplary—clearly stating that the centralized and global-state mesh baselines are intentional bounds, not realistic competitors, prevents the most common misinterpretation of such comparisons. The M/D/c sensitivity table (Table I) further reinforces this by showing that parallelized ground systems scale trivially.

The three DES-unique contributions are well-supported:

1. **Coordinator capacity sizing** (Tables VII–VIII): The 50 kbps vs. 24 kbps finding is cleanly derived from the random-phase vs. TDMA comparison, and the physical interpretation (2.5× headroom for burstiness) is correct. The TDMA analysis (Eq. 15) is straightforward but useful.

2. **AoI characterization** (Table IX, Fig. 8): The geometric inter-report distribution under Bernoulli exception filtering is correctly modeled, and the orbital context (440 s → ~2.8 km along-track uncertainty) is appropriately qualified as "order-of-magnitude." The authors correctly note that AoI measures freshness, not accuracy.

3. **Gilbert-Elliott analysis** (Section IV-K): The 27% vs. 87.5% retransmission recovery comparison is the paper's most impactful finding. The physical interpretation—that bad-state persistence across all retry attempts within a cycle makes intra-cycle retransmission "structurally ineffective"—is correct and has clear design implications for DTN/BPv7 adoption.

One logical concern: the paper claims the hierarchical architecture is validated to 10⁵ nodes, with analytical extrapolation to 10⁶ shown in Fig. 3. However, since the DES operates at the message-passing layer and the overhead is analytically $O(1)$, the "validation" at 10⁵ is no more informative than at 10³—the interesting question is whether physical-layer effects (MAC contention, link acquisition, antenna scheduling) introduce scale-dependent overhead, and this is precisely what the DES does not model. The extrapolation to 10⁶ should be more strongly caveated.

The treatment of the sectorized mesh as an "intermediate decentralized architecture" is logically sound, and the observation that it converges architecturally toward the hierarchical model (Section V-A) is insightful. However, the overhead comparison (65–67% vs. 46%) is specific to the capped-fanout parameterization and the stress-case workload; under the nominal workload, the comparison would be different and should be reported.

---

## 4. Clarity & Structure

**Rating: 4 (Good)**

The paper is well-organized and generally well-written, with a logical flow from problem statement through methodology, results, and discussion. The extensive use of tables (12 tables) and figures (11 figures) supports the quantitative arguments effectively. The traffic accounting tables (Tables IV, V, VI) and the abstraction scope table (Table VI) are particularly valuable for reproducibility.

Several structural strengths deserve recognition:
- The explicit separation of baseline telemetry (20.5%, topology-invariant) from protocol overhead ($\eta$) is clearly maintained throughout.
- The distinction between "delivered" and "offered" overhead in Table X is important and well-explained.
- The latency budget decomposition (Section IV-B) identifying regional coordinator burstiness as the dominant component is informative.

However, the paper suffers from excessive length and redundancy. At approximately 12,000 words of body text plus extensive tables and figures, it substantially exceeds typical IEEE T-AES page limits. Several passages repeat information:
- The baseline interpretation caveat appears in the abstract, Section I-C, Section III-B-1, Section IV-A, and Section V-C—at least three of these could be consolidated.
- The $\eta \approx 46\%$ figure is stated in the abstract, contributions list, Section IV-D, Table VIII, and the conclusion.
- The MAC efficiency adjustment ($\eta_{\text{eff}} \in [51\%, 66\%]$) is repeated at least six times.

The abstract is accurate but dense—it attempts to summarize all five contributions in quantitative detail, which may overwhelm readers. A more focused abstract highlighting the three DES-unique findings would be more effective.

Minor clarity issues: The notation switches between $M_r$ and $M_{\text{retry}}$ for maximum retransmissions (compare Eq. 8 with Table X header). The collision avoidance rate footnote (Table II, note a) is important context that could be elevated to the main text.

---

## 5. Ethical Compliance

**Rating: 5 (Excellent)**

The paper provides exemplary transparency regarding AI-assisted methodology. The Acknowledgment section clearly identifies the AI tools used (Claude 4.6, Gemini 3 Pro, GPT-5.2), describes their role as "exploratory AI-assisted ideation," references a companion methodology paper, and explicitly states that the AI-generated concepts "are not validated in the current study." This level of disclosure exceeds current IEEE requirements and sets a good standard.

The anonymous authorship ("Project Dyson Research Team") with a note that individual names will be provided for final publication is acceptable for review but must be resolved before publication per IEEE policy. The data availability statement with a GitHub repository link (pending commit hash) supports reproducibility. No conflicts of interest are apparent, and the research does not raise ethical concerns regarding dual-use or environmental impact.

---

## 6. Scope & Referencing

**Rating: 3 (Adequate)**

The paper is appropriate for IEEE T-AES in scope, addressing autonomous spacecraft coordination at scale—a topic of growing relevance as mega-constellations expand. The reference list (48 citations) covers the major relevant areas: constellation operations, swarm robotics, distributed systems theory, queueing theory, and DTN.

However, several referencing gaps exist:

**Missing recent work on autonomous constellation management.** The paper does not cite recent work on autonomous satellite operations, including ESA's OPS-SAT experiments, NASA's Starling mission (4-CubeSat autonomous swarm demonstration, 2023), or the growing literature on onboard autonomous collision avoidance (e.g., Merz et al., 2017; Bombardelli et al., 2021). The Starling mission is particularly relevant as it demonstrated autonomous swarm coordination in LEO at small scale.

**DTN/space networking literature.** While Cerf et al. (RFC 4838) and BPv7 are cited, the substantial body of work on DTN performance in LEO constellations (e.g., Fraire et al., 2021; Caini and Firrincieli, 2011) is missing. Given that the GE analysis concludes store-and-forward is required, this literature is directly relevant.

**Age of Information in space systems.** The AoI citations (Kaul, Yates, Kadota) are foundational but terrestrial. Recent work applying AoI to satellite networks (e.g., Leyva-Mayorga et al., 2022; Abd-Elmagid et al., 2020) should be acknowledged.

**Non-archival references.** Several references (SpaceX Starlink operations, Amazon Kuiper, DARPA OFFSET, DARPA Blackjack, DoD Replicator) are non-archival web pages. While the authors note "non-archival; accessed February 2026," IEEE T-AES generally prefers archival sources. The NRL swarm reference is described as a "magazine article, non-peer-reviewed."

**Self-citation.** The companion methodology paper [42] is cited but appears to be a non-peer-reviewed project publication. Its role in the current paper is appropriately limited to the Acknowledgment.

---

## Major Issues

1. **Limited value-add of DES over closed-form analysis.** The headline result ($O(1)$ overhead at ~46%) is analytically derivable and the DES confirms it to 0.1%. The three genuinely DES-unique contributions (coordinator capacity, AoI, GE loss) are valuable but could be presented more concisely. The paper should either (a) restructure to lead with the DES-unique findings and relegate the overhead verification to a validation appendix, or (b) add physical-layer coupling (even simplified) that would make the DES indispensable. As currently structured, the paper risks the criticism that a 25-page simulation study was unnecessary for results obtainable from a spreadsheet.

2. **Absence of packet-level or physical-layer validation.** The MAC efficiency factor $\gamma \in [0.7, 0.9]$ is assumed, not derived. The coordinator bandwidth thresholds (24–50 kbps) are offered-load requirements that must be adjusted for physical-layer effects before engineering application. Without at least a single-cluster packet-level validation (which the authors identify as priority future work), the "actionable design parameters" claimed in the conclusion cannot be directly applied to hardware link budgets. This gap should be explicitly acknowledged as a limitation on the precision of the quantitative results.

3. **Stress-case workload dominance and questionable operational relevance.** The stress-case workload (one 512-byte command per node per cycle) drives the headline 46% overhead but is acknowledged as "a conservative upper bound unlikely to be sustained indefinitely." The nominal workload produces only 5% overhead. The paper should more clearly frame which workload is relevant for which operational scenario, and the sectorized mesh comparison should be reported under all three workload profiles, not just the stress case.

4. **Regional coordinator parameters unswept.** The number of regional coordinators ($n_r = 10$) and their processing capacity ($\mu_r = 500$ msg/s) are identified as "first-order design variables" but are not swept. Since regional coordinator burstiness dominates the 508 ms mean latency, this is a significant omission. The paper should either sweep these parameters or provide analytical bounds on the latency as a function of $n_r$.

---

## Minor Issues

1. **Notation inconsistency.** $M_r$ vs. $M_{\text{retry}}$ for maximum retransmissions (Eq. 8 vs. Table X). Standardize throughout.

2. **Table VIII intermediate rows.** The statement "omitted for brevity" for 8 intermediate fleet sizes is acceptable but the table could simply show 3–4 representative sizes rather than claiming omission.

3. **Fig. 3 extrapolation.** The 10⁶-node curve is labeled as "analytical extrapolation" in the caption but may be misread as DES-validated. Consider using a distinct line style (e.g., dotted with explicit "EXTRAPOLATION" label) or removing it entirely.

4. **Section III-F, paragraph 2.** "At $10^5$ nodes, even 1 kbps/node aggregates to 100 Mbps fleet-wide"—this should be "100 Mbps" (confirmed correct: $10^5 \times 10^3 = 10^8$ bps = 100 Mbps).

5. **Table II footnote c.** "Server processing capacity $\mu_s$ (messages/s); distinct from link bandwidth $C_{\text{node}}$ (kbps)"—this clarification should appear at first use of $\mu_s$ in the main text, not only in a table footnote.

6. **Eq. 4 convergence time.** The claim $D = O(N^{1/3})$ for a random geometric graph in 3D orbital space is stated without proof or reference. In practice, LEO constellations are distributed on a thin spherical shell (effectively 2D), where $D = O(N^{1/2})$. This should be corrected or justified.

7. **Section IV-C.** The handoff success rate at 1-hour duty cycle (95.0%) is stated to arise from "cumulative probability of at least one handoff failure per day reaches 5%." This should be derived: if per-handoff success is $p_h$ and there are 24 handoffs/day, then daily success = $p_h^{24} = 0.95$, giving $p_h = 0.95^{1/24} \approx 0.9979$. The per-handoff success rate should be stated explicitly.

8. **Reference [42] (companion paper).** The URL points to a project website, not an archival publication. If this paper is under review or in preparation, it should be cited as such.

9. **Abstract length.** At ~280 words, the abstract exceeds the IEEE T-AES recommended limit of ~200 words. Consider trimming.

10. **Table III latency values.** The discrete jumps (340 ms vs. 508 ms vs. 675 ms) suggest quantized behavior that should be explained more prominently—the explanation in the latency budget paragraph is good but could be referenced directly from the table.

---

## Overall Recommendation

**Major Revision**

This paper addresses a relevant problem and demonstrates careful, transparent engineering analysis. The three DES-unique contributions (coordinator capacity sizing, AoI-bandwidth trade-off, and Gilbert-Elliott retransmission ineffectiveness) are genuinely useful for space systems designers. However, the paper's primary weakness is that the bulk of its content (overhead scaling verification, topology comparison) confirms analytically predictable results through simulation, while the novel simulation-dependent findings are somewhat buried. The absence of any physical-layer validation limits the applicability of the quantitative design parameters claimed. A major revision should restructure the paper to foreground the DES-unique contributions, add the regional coordinator parameter sweep, provide at least a simplified physical-layer coupling or packet-level validation for one cluster, and reduce overall length by ~30%. The sectorized mesh comparison should be extended to all workload profiles. With these changes, the paper would make a solid contribution to IEEE T-AES.

---

## Constructive Suggestions

1. **Restructure around DES-unique findings.** Reorganize the paper so that the three genuinely simulation-dependent results (coordinator capacity sizing with burstiness analysis, AoI-bandwidth trade-off quantification, and GE correlated loss characterization) are the primary contributions, presented first and in greatest detail. Relegate the $O(1)$ overhead verification to a concise validation section. This would sharpen the novelty claim and reduce redundancy.

2. **Add a single-cluster packet-level validation.** Even a simplified NS-3 or OMNeT++ simulation of one 100-node cluster with realistic TDMA scheduling would ground the MAC efficiency assumption ($\gamma$) and validate the coordinator bandwidth thresholds. This would transform the "actionable design parameters" from offered-load estimates to engineering specifications.

3. **Sweep regional coordinator parameters.** Since regional burstiness dominates latency (500 ms of the 508 ms total), sweeping $n_r \in \{5, 10, 20, 50\}$ and $\mu_r \in \{200, 500, 1000\}$ would characterize the most important latency design lever. Also model phase-offset cluster reporting, which the authors identify as a latency reduction mechanism but do not evaluate.

4. **Report sectorized mesh under all workload profiles.** The current comparison (65–67% sectorized vs. 46% hierarchical) uses only the stress-case workload. Under the nominal workload (5% hierarchical), the sectorized mesh overhead and the relative comparison may be quite different. Providing this comparison would strengthen the architectural analysis.

5. **Reduce paper length by ~30%.** Consolidate the repeated baseline interpretation caveats into a single prominent subsection. Merge Tables VII and VIII into a single coordinator capacity summary. Remove or substantially shorten the analytical cross-check derivation (Eq. 13 and surrounding text), which confirms code correctness rather than constituting a finding. Target ~9,000 words of body text to meet IEEE T-AES norms.