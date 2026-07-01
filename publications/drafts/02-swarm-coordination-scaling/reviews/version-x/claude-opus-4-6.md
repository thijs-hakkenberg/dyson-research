---
paper: "02-swarm-coordination-scaling"
version: "x"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-24"
recommendation: "Major Revision"
---



# Peer Review: "Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study"

---

## 1. Significance & Novelty

**Rating: 3 (Adequate)**

The paper addresses a genuinely important problem: how to coordinate autonomous spacecraft swarms at scales of 10³–10⁵ nodes, a regime that is underexplored in the literature. The framing around mega-constellation growth (Starlink, Kuiper) is timely, and the explicit byte-level traffic accounting approach is a useful engineering contribution that distinguishes this work from purely analytical or heuristic studies. The identification of three DES-unique contributions—coordinator capacity sizing, AoI-bandwidth trade-offs, and correlated loss characterization—represents a reasonable attempt to articulate what simulation adds beyond closed-form analysis.

However, the novelty is substantially diluted by the paper's own admissions. The $O(1)$ overhead scaling is described as "a direct mathematical consequence of the hierarchical message structure—not a surprising emergent property" (Section IV-D). The DES-to-analytical agreement of <0.1% (Table V, Section IV-D-2) confirms that the simulation is essentially computing the same closed-form sums as Eq. (12), with MC variance of SD < 0.001%. The authors are commendably transparent about this, but it raises the question: what does the DES actually discover that could not be derived analytically? The coordinator capacity sizing result (50 kbps unscheduled vs. 24 kbps TDMA) is essentially a burstiness analysis of Poisson arrivals against a deadline-constrained buffer—a well-understood queueing result. The AoI analysis follows directly from the geometric distribution of inter-report intervals. The Gilbert-Elliott retransmission result (27% vs. 87.5% recovery) is likewise analytically derivable from the state-conditional loss probabilities.

The gap claim in the introduction—"no prior work has systematically compared coordination architectures for autonomous spacecraft swarms across the 10³–10⁵ range"—is somewhat overstated. While the specific combination of byte-level accounting and autonomous coordination at this scale may be novel, the individual components (hierarchical aggregation, gossip protocols, queueing analysis of coordinators) are well-established. The paper would benefit from more precisely delineating what is genuinely new versus what is a competent synthesis of known techniques applied to a new domain.

---

## 2. Methodological Soundness

**Rating: 3 (Adequate)**

The cycle-aggregated DES framework is clearly described and the abstraction level is well-justified for the research questions posed. The full-participation simulation (all N nodes active every cycle), the explicit traffic accounting (Table IV), and the analytical cross-check (Section IV-D-2) are methodological strengths that support reproducibility and internal consistency. The Monte Carlo framework with 30 replications per configuration is appropriate, and the authors' candid acknowledgment that MC variance is negligible (SD < 0.001%) is refreshing.

However, several methodological concerns arise:

**Near-tautological validation.** The DES implements the same traffic accounting as the closed-form model (Eq. 12), so the <0.1% agreement is a code-correctness check, not an independent validation. The authors acknowledge this ("validates implementation correctness rather than constituting an independent finding"), but the paper's structure—presenting this as a primary result in Table V and Section IV-D-2—overstates its significance. A more meaningful validation would compare against a packet-level simulator (NS-3, OMNeT++) for at least one configuration, which the authors identify as future work but which would substantially strengthen the current submission.

**Baseline construction.** The centralized baseline ($c=1$, $\mu_s = 1000$ msg/s) is acknowledged as an intentional worst case, and the M/D/c sensitivity analysis (Table I) partially addresses this. However, the global-state mesh baseline assumes every node must maintain full trajectory state for all $O(N)$ peers—a requirement that no operational system would impose. The sectorized mesh is a welcome addition that partially fills this gap, but its capped-fanout variant ($\leq 10$ heartbeat neighbors) is itself a hybrid hierarchical-mesh architecture with sector coordinators, making the comparison less clean than presented. The paper would benefit from acknowledging more explicitly that the "hierarchical vs. sectorized mesh" comparison is really "pure hierarchy vs. hierarchy + peer heartbeats."

**Stochastic model limitations.** The Bernoulli link loss model and the Gilbert-Elliott extension are reasonable first-order approximations, but the 10-second GE state transition discretization is coarse. More importantly, the failure model (i.i.d. exponential, 2%/year) is acknowledged as a best case but is never stress-tested against correlated failures—a critical gap for space systems where solar particle events can simultaneously degrade multiple spacecraft. The collision avoidance event rate ($10^{-4}$/node/s) is justified by the screening-to-maneuver ratio, but the sensitivity analysis (varying from $10^{-5}$ to $10^{-3}$) shows only ±1.5 percentage points of overhead change, suggesting this parameter has minimal impact on the results—which further questions what the DES reveals beyond the dominant command/heartbeat terms.

**Cluster size results.** Table III shows overhead varying by only ±0.1% across $k_c = 50$–500, which the authors correctly attribute to the dominance of per-node command traffic. However, this means the cluster size "optimization" is essentially a latency analysis, and the latency values show discrete jumps (508→675 ms at $k_c < 100$) rather than smooth trade-offs. The mechanism (regional coordinator burst arrivals) is plausible but the discrete jumps suggest the model may be too coarse to capture the actual sensitivity.

---

## 3. Validity & Logic

**Rating: 3 (Adequate)**

The paper's logical structure is generally sound, and the authors are commendably transparent about the limitations of their approach. The distinction between "DES-measured" and "analytically projected" results is consistently maintained, and the baseline interpretation note (Section I-C) appropriately frames the reference architectures as bounds rather than competitors.

Several logical concerns merit attention:

**Circular reasoning in overhead claims.** The headline result—$\eta \approx 46\%$ stress-case overhead—is driven almost entirely by the assumption that every cluster coordinator sends a unique 512-byte command to every member every cycle. This is explicitly acknowledged as a "conservative stress-case assumption" (Section IV-D-2), yet it drives the primary metric throughout the paper. The nominal workload ($\eta \approx 5\%$) is arguably more representative of sustained operations, but receives far less attention. The paper would be more balanced if the nominal case were presented as the primary result with the stress case as an upper bound, rather than the reverse.

**AoI interpretation.** The AoI analysis (Section IV-E) correctly identifies the geometric distribution of inter-report intervals under exception-based telemetry, and the orbital context (2.8 km along-track uncertainty at 440s AoI) is a valuable engineering translation. However, the claim that this "requires mission-specific trade-off against conjunction screening timelines" is somewhat vacuous—of course it does. A more useful contribution would be to derive the conjunction detection probability degradation as a function of AoI, which the authors identify as future work (Section V-B, item 1). Without this coupling, the AoI results are descriptive rather than prescriptive.

**Sectorized mesh comparison.** The sectorized mesh overhead of 65–67% vs. hierarchical 46% is presented as evidence that "peer-to-peer heartbeats add significant cost." However, the sectorized mesh also includes coordinator-to-member commands (512 B each, matching the hierarchical workload), so the 19–21 percentage point difference is attributable to the 10 × 32 B = 320 B of heartbeats per node per cycle—which is only 2.6% of the 1 kbps channel. The remaining difference must come from inter-sector relay traffic. The decomposition is not clearly presented, making it difficult to assess the claimed "1.4–1.5× hierarchical" ratio.

**Extrapolation beyond validated range.** Fig. 2 includes a $10^6$-node analytical extrapolation that is appropriately flagged as "not DES-measured." However, the paper's title and abstract focus on $10^3$–$10^5$, and the introduction mentions $10^5$–$10^6$ aspirational scales. The gap between the validated range and the motivating scale is significant and should be more prominently acknowledged.

---

## 4. Clarity & Structure

**Rating: 4 (Good)**

The paper is well-organized and generally well-written, with a logical progression from problem statement through methodology, results, and discussion. The extensive use of tables (12 tables) and figures (11 figures) supports the quantitative arguments, and the consistent traffic accounting framework (Table IV) is a structural strength. The abstract accurately summarizes the three main contributions, and the baseline interpretation note (Section I-C) is a valuable framing device.

Several clarity issues deserve attention:

**Length and redundancy.** At approximately 12,000 words of body text plus extensive tables and figures, the paper is long for a journal submission. There is significant redundancy: the $\eta \approx 46\%$ figure is stated at least 15 times across the abstract, introduction, results, and conclusion. The traffic accounting is explained in Section III-F, re-derived in Section IV-D-2, and summarized again in Table II. Consolidating these discussions would improve readability without sacrificing rigor.

**Notation consistency.** The paper uses $C_{\text{node}}$ for per-node bandwidth, $C_{\text{coord}}$ for coordinator capacity, $\mu_s$ for server processing rate, and $\gamma$ for MAC efficiency—all reasonable choices, but the proliferation of capacity-related symbols can be confusing. A notation table would help. The distinction between "offered load" and "delivered overhead" (Table VII) is important but introduced late; it should be established earlier.

**Figure quality.** The figures are referenced but not included in the LaTeX source (placeholder PDFs). Based on the captions, they appear well-designed with appropriate axis labels and annotations. Fig. 1 (architecture diagram) and Fig. 5 (AoI quality) seem particularly valuable. However, Fig. 2 (latency distribution) includes the $10^6$ extrapolation in the same visual frame as DES-validated results, which could mislead readers despite the caption disclaimer.

**Section V organization.** The Discussion section (V) is relatively brief compared to the Results section (IV), and the "Unresolved Questions" subsection (V-B) reads more like a future work section. The sectorized mesh discussion (V-A) makes an interesting architectural convergence argument that deserves more development.

---

## 5. Ethical Compliance

**Rating: 4 (Good)**

The paper includes an appropriate acknowledgment of AI-assisted ideation (Claude 4.6, Gemini 3 Pro, GPT-5.2) in the Acknowledgment section, with a clear statement that the AI-generated concepts are "not validated in the current study." The data availability statement provides a GitHub repository URL (with pending commit hash), which is commendable for reproducibility. The anonymous authorship ("Project Dyson Research Team") with a note about IEEE policy compliance is acceptable for review but must be resolved for publication.

One minor concern: the Acknowledgment references "Claude 4.6" and "GPT-5.2," which do not correspond to publicly released model versions as of the review date. If these are internal or pre-release designations, this should be clarified. The companion methodology paper [45] is cited but appears to be a self-published working paper rather than a peer-reviewed publication; its status should be clarified.

The 2% annual failure rate assumption is attributed to Castet and Saleh [28], which is appropriate. The collision avoidance event rate justification via ESA Space Debris Office data [47] is well-sourced. No conflicts of interest are apparent, though the institutional affiliation ("Project Dyson") is not a recognized research institution—the authors should clarify whether this is an academic, industry, or independent research group.

---

## 6. Scope & Referencing

**Rating: 3 (Adequate)**

The paper is appropriate for IEEE Transactions on Aerospace and Electronic Systems in terms of topic (autonomous spacecraft coordination) and methodology (simulation-based systems engineering). The reference list (48 citations) covers the relevant literature across constellation management, swarm robotics, distributed systems, and queueing theory.

However, several referencing gaps are notable:

**Missing recent work.** The paper does not cite recent work on distributed space systems coordination that has appeared since 2020, including publications on autonomous constellation management from MIT Lincoln Laboratory, Surrey Space Centre, and the European Space Agency's OPS-SAT mission. The CCSDS Proximity-1 protocol [37] is cited but the more recent CCSDS DTN implementations and IOAG interoperability standards are not discussed.

**Non-archival sources.** Several key references are non-archival: SpaceX Starlink operations [1], Amazon Kuiper [3], DARPA OFFSET [20], DARPA Blackjack [39], and DoD Replicator [22]. While these are appropriate for contextual motivation, the paper relies on them for claims about current operational scales. The NRL swarm reference [21] is explicitly noted as "non-peer-reviewed."

**Queueing theory depth.** The M/D/1 and M/D/c models are well-cited via Kleinrock [27], but the deadline-constrained byte budget model for coordinator ingress (Section IV-G) is not connected to the established literature on deadline-constrained scheduling or real-time queueing. The AoI literature is cited via Kadota et al. [48], but the broader AoI scheduling literature (Yates, Kaul, Sun & Modiano) is not referenced.

**Mean-field game theory.** The citations to Lasry & Lions [16] and Huang et al. [17] are appropriate but the connection to the current work is tenuous—the paper does not use mean-field methods. These citations appear to be included for completeness rather than relevance.

---

## Major Issues

1. **The DES adds limited value beyond closed-form analysis.** The <0.1% agreement between DES and analytical predictions (Table V), combined with SD < 0.001% MC variance, demonstrates that the simulation is essentially computing the same deterministic sums as the traffic accounting model. The three claimed DES-unique contributions (coordinator capacity, AoI, GE loss) are all analytically derivable from the assumed models. The paper needs either (a) a packet-level validation that demonstrates phenomena not captured by the message-layer abstraction, or (b) a more honest framing that this is primarily an analytical design-space characterization with DES serving as a verification tool.

2. **The stress-case workload assumption dominates all results but is poorly justified.** The assumption that every coordinator sends a unique 512-byte command to every member every cycle is the single largest driver of the 46% overhead figure. No operational scenario is described that would require this sustained rate. The paper should either justify this rate from operational requirements or reframe the nominal workload (5%) as the primary result.

3. **The baseline comparisons are structurally unfair despite disclaimers.** While the authors repeatedly note that baselines are "intentional bounds," the visual presentation (Fig. 1, Fig. 7) and table structure (Table II) inevitably invite direct comparison. The single-server centralized baseline ($c=1$) is a straw man that no real system would deploy at scale; the global-state mesh requires $O(N^2)$ communication that no practical system would implement. The sectorized mesh is the only meaningful comparator, and it is itself a hierarchical variant. The paper should either (a) include a realistic parallelized centralized baseline ($c=100$) in the DES, or (b) restructure the paper as a pure parametric characterization of the hierarchical architecture without comparative claims.

4. **No packet-level or physical-layer validation.** The MAC efficiency factor $\gamma \in [0.7, 0.9]$ is applied as a post-hoc correction but is never validated. The abstraction table (Table VI) lists 10 unmodeled phenomena, several of which (link acquisition, antenna beam scheduling, half-duplex turnaround) could introduce scale-dependent effects that would invalidate the $O(1)$ overhead claim at the physical layer. At minimum, a single-cluster packet-level simulation should be included.

---

## Minor Issues

1. **Section III-A, paragraph 2:** "Events at both resolutions are managed through a single priority queue ordered by simulated time; one-second resolution applies only to collision avoidance events"—this implies a hybrid time-step/event-driven architecture that is not clearly described. Is the simulation truly event-driven or cycle-stepped with sub-cycle resolution for collision events?

2. **Eq. (4), hierarchical messages:** The equation counts only uplink reporting; the text notes that "downward command traffic approximately doubles the overhead." This factor-of-two discrepancy between the equation and the actual overhead should be resolved by presenting the full bidirectional message count equation.

3. **Table III (cluster size sensitivity):** The latency values show only two discrete levels (340 ms and 508 ms for $N=10^4$; 508 ms and 675 ms for $N=10^5$). This suggests a quantization artifact in the simulation rather than a smooth physical relationship. The mechanism should be explained more clearly.

4. **Section IV-E (AoI):** The "orbital context" paragraph converts 440s AoI to ~2.8 km along-track uncertainty using "6–8 m/s" perturbation growth rate. This rate should be cited or derived; it appears to conflate differential drag (which depends on ballistic coefficient differences) with $J_2$ secular drift (which depends on semi-major axis differences).

5. **Table VII (link availability):** The "Offered" column for $M_r = 2$ at $p_{\text{link}} = 0.4$ shows 90.2%, but the footnote states total offered including baseline exceeds 100% at $p_{\text{link}} \leq 0.5$. The threshold should be stated consistently.

6. **Section III-G (communication overhead definition):** The statement "exceeds the throughput limit of random access protocols (~36% for Slotted ALOHA)" is correct but the 36% figure applies to normalized throughput, not channel utilization. The comparison should be more precise.

7. **Eq. (12):** The term $N(0.128)$ for collision avoidance appears to use the rate $10^{-4} \times 10 \times 128 = 0.128$ B/node/cycle, but this should be $10^{-4} \times 10 \times 128 = 0.128$ B—confirm units are bytes, not bits.

8. **References [1], [3], [20], [22], [39]:** These non-archival web sources should include access dates consistently. Some show "accessed February 2026" which appears to be a future date relative to the manuscript preparation.

9. **Abstract:** "Age-of-Information tracking shows that exception-based telemetry at $p_{\text{exc}} = 0.10$ reduces protocol overhead from 46% to ~5%"—this conflates two different mechanisms (exception telemetry reduces reporting frequency; AoI measures the consequence). The abstract should state these as cause and effect more clearly.

10. **Section III-B-2:** The handoff state size is "10–50 MB, depending on cluster size" but the formula $s_{\text{handoff}} = 100 \times k_c$ KB gives 10 MB at $k_c = 100$ and 50 MB at $k_c = 500$. The 100 KB/node scaling factor should be justified.

---

## Overall Recommendation

**Major Revision**

This paper addresses a relevant and timely problem—coordination scaling for large autonomous spacecraft swarms—and presents a well-structured parametric analysis with commendable transparency about assumptions and limitations. The byte-level traffic accounting framework, the AoI-bandwidth trade-off characterization, and the Gilbert-Elliott correlated loss analysis are useful engineering contributions. However, the paper's central methodological tool (the cycle-aggregated DES) adds negligible value beyond closed-form analysis, as demonstrated by the <0.1% DES-to-analytical agreement and near-zero MC variance. The baseline comparisons, despite extensive disclaimers, remain structurally unfair. The stress-case workload assumption that drives the headline 46% overhead figure is poorly motivated operationally. A major revision should: (1) reframe the paper as a parametric design-space characterization rather than a simulation study, or include packet-level validation for at least one configuration; (2) present the nominal workload as the primary result; (3) either include a realistic parallelized centralized baseline in the DES or remove comparative claims; and (4) couple the AoI analysis to conjunction detection probability to deliver prescriptive rather than descriptive results.

---

## Constructive Suggestions

1. **Include a single-cluster packet-level validation.** Run one configuration ($k_c = 100$, one coordination cycle) through NS-3 or OMNeT++ with realistic optical ISL parameters to validate the MAC efficiency assumption and demonstrate that the message-layer abstraction captures the relevant physics. This would transform the paper from "we computed traffic accounting and verified it with a simulator that computes the same accounting" to "we validated that message-layer accounting accurately predicts physical-layer behavior."

2. **Derive conjunction detection probability as a function of AoI.** Couple the AoI distribution to a simplified $J_2$-perturbed orbital propagation model to compute the probability of missing a conjunction event as a function of $p_{\text{exc}}$. This would make the AoI results actionable for mission designers rather than requiring them to perform the coupling themselves. Even a simplified analytical model (linear along-track uncertainty growth, Gaussian miss-distance distribution) would substantially increase the paper's practical value.

3. **Restructure around the workload envelope rather than the stress case.** Present the three workload profiles (stress, nominal, event-driven) as co-equal results defining a design envelope, rather than leading with the stress case. The $9\times$ spread ($5\%$–$46\%$) is itself the most interesting finding—it tells system designers that control-plane sizing is dominated by workload assumptions, not architecture choice. This reframing would also reduce the paper's dependence on the questionable per-node-per-cycle command assumption.

4. **Replace or supplement the single-server centralized baseline with a parallelized version.** Add $c = 10$ and $c = 100$ centralized baselines to the DES (not just Table I) so that readers can see the actual scaling behavior of a realistic centralized system. This would make the hierarchical architecture's advantages (latency, autonomy, fault tolerance) more clearly attributable to architectural properties rather than baseline handicapping.

5. **Tighten the paper by 25–30%.** The current manuscript is excessively long with significant redundancy. Consolidate the traffic accounting discussion (currently spread across Sections III-F, III-G, III-H, and IV-D-2), reduce the number of times $\eta \approx 46\%$ is restated, and move the sectorized mesh details to an appendix. This would improve readability and allow space for the packet-level validation or AoI-conjunction coupling suggested above.