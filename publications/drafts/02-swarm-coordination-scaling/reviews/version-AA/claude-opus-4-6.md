---
paper: "02-swarm-coordination-scaling"
version: "AA"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-26"
recommendation: "Major Revision"
---



# Peer Review: "Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study"

**Manuscript Version:** AA
**Venue:** IEEE Transactions on Aerospace and Electronic Systems

---

## 1. Significance & Novelty

**Rating: 3 (Adequate)**

The paper addresses a genuinely important problem: how to coordinate autonomous spacecraft swarms at scales of 10³–10⁵ nodes, a regime that is underexplored in the literature. The authors correctly identify that current constellation management (Starlink, OneWeb) relies on centralized ground control and that scaling to 10⁵+ nodes will require fundamentally different coordination architectures. The framing around byte-level traffic accounting under a fixed per-node budget is a useful engineering lens that distinguishes this work from more abstract multi-agent coordination studies.

However, the novelty is more limited than the authors suggest. The $O(1)$ overhead scaling of the hierarchical architecture (with fixed hierarchy depth and fixed cluster size) is, as the authors themselves acknowledge, "a direct mathematical consequence of the hierarchical structure" (Section IV-E). The DES essentially confirms what the analytical model already predicts, with <0.1% discrepancy. The three DES-unique contributions (coordinator burstiness, AoI characterization, GE loss recovery) are individually modest: the burstiness result is a straightforward consequence of random-phase superposition vs. TDMA; the AoI result follows directly from the geometric distribution of inter-report intervals under exception-based telemetry; and the GE loss result ($1 - 0.9^3 = 27.1\%$) is analytically trivial. The value lies in assembling these into a coherent design-space characterization, but each individual finding could be derived in a few lines of analysis.

The claim in Section I-A that "no prior work has systematically compared coordination architectures for autonomous spacecraft swarms across the 10³–10⁵ range" may be overstated. While the specific combination of byte-level accounting, autonomous coordination, and this scale range may be novel, the individual components (hierarchical vs. flat coordination, gossip protocol analysis, queueing models for satellite networks) are well-established. The paper would benefit from a more measured novelty claim.

---

## 2. Methodological Soundness

**Rating: 2 (Needs Improvement)**

The cycle-aggregated DES framework is clearly described and the parameter space is well-documented (Table III is commendably thorough). The Monte Carlo framework with 30 replications per configuration is appropriate, and the authors are refreshingly honest that the near-deterministic message model renders the MC framework largely confirmatory (SD < 0.001%). The validation against M/D/1 analytical solutions and gossip convergence bounds is a positive feature.

However, several methodological concerns are significant:

**The simulation is too abstract to generate actionable engineering results.** The DES operates at the message-passing layer and abstracts away MAC-layer scheduling, link acquisition, pointing constraints, Doppler effects, orbital mechanics perturbations, half-duplex turnaround, antenna beam scheduling, and priority queueing (Table V). While the authors acknowledge these abstractions, the gap between the simulation and physical reality is so large that the reported overhead percentages and coordinator bandwidth thresholds cannot be directly applied to system design. The MAC efficiency factor γ ∈ [0.7, 0.9] is essentially a fudge factor that spans a 30% range—this uncertainty dominates the precision of the DES results. The authors note that "packet-level validation via NS-3 or OMNeT++" is a future direction, but without it, the quantitative results are difficult to trust for hardware link budget purposes.

**The comparison architecture is structurally biased.** The centralized baseline uses a single-server model ($c = 1$) that the authors acknowledge is an "intentional worst-case bound." The global-state mesh requires full fleet state replication, which the authors acknowledge "is an intentional upper bound on decentralized overhead, not a realistic architecture." While the authors are transparent about these choices and provide the sectorized mesh as an intermediate comparator, the paper's structure still implicitly frames the hierarchical architecture as superior by bracketing it between two deliberately extreme baselines. The sectorized mesh comparison is more meaningful, but the capped-fanout variant (cap = 10, monitoring only 3.2% of sector peers) may be too restrictive to provide equivalent conjunction screening capability, making the overhead comparison potentially unfair.

**The 1 kbps per-node budget is not well-justified as a universal constraint.** The authors argue it represents a fallback RF constraint during optical link outages, but the coordination protocol's behavior during optical operation (the dominant mode) would be qualitatively different. Designing the entire coordination architecture around the worst-case fallback link seems overly conservative and may distort the architecture comparison. A dual-mode analysis (nominal optical + degraded RF) would be more informative.

**The collision avoidance event rate of 10⁻⁴/node/s deserves more scrutiny.** While the authors provide a reasonable justification (1000:1 screening-to-maneuver ratio), this rate generates ~1 alert per node per ~2.8 hours, which seems high for a swarm where most nodes are in non-intersecting orbital planes. The sensitivity analysis (varying from 10⁻⁵ to 10⁻³) is appreciated but shows only that the qualitative ranking is preserved—it does not validate the baseline rate.

---

## 3. Validity & Logic

**Rating: 3 (Adequate)**

The internal logic of the paper is generally sound. The analytical predictions match the DES results to within 0.1%, which validates the implementation but also raises the question of what the DES adds beyond the analytical model. The three DES-unique contributions (burstiness, AoI, GE losses) are correctly derived and interpreted.

The authors are commendably transparent about limitations. The "Baseline Interpretation Note" (Section I-C), the explicit acknowledgment that the centralized and mesh baselines are intentional bounds, the detailed abstraction scope table (Table V), and the honest discussion of unresolved questions (Section V-A) all demonstrate intellectual honesty that strengthens the paper.

However, several logical issues deserve attention:

**The $O(1)$ overhead claim requires qualification.** The overhead is $O(1)$ only because the hierarchy depth is fixed at 4 levels and the cluster size $k_c$ is fixed. If the hierarchy were allowed to grow with $N$ (e.g., adding levels for $N > 10^5$), the scaling would change. The authors should clarify that $O(1)$ applies within the fixed-architecture regime they study, not as a general property of hierarchical coordination.

**The sectorized mesh comparison conflates architecture and workload differences.** The sectorized mesh includes peer heartbeats (32 B × 10 neighbors) that the hierarchical architecture does not require because the coordinator aggregates state. But this means the sectorized mesh provides different (arguably better) local state awareness—each node monitors 10 peers directly rather than relying on coordinator-mediated summaries. The 1.4–1.5× overhead ratio is meaningful only if the two architectures provide equivalent coordination quality, which is not established.

**Table VII (cluster size sensitivity) shows suspiciously uniform results.** Overhead varies by only ±0.1% across $k_c = 50$–500, and latency shows only two discrete values (340 ms and 508 ms for $N = 10^5$). The step function in latency suggests the simulation may be discretizing queueing effects too coarsely. The latency decomposition (propagation + processing + queueing) should produce a smoother curve as $k_c$ varies.

**The extrapolation to 10⁶ nodes (Fig. 8) is acknowledged as analytical but may mislead readers.** The figure caption notes this, but the visual presentation on the same plot as DES-validated results could create a false impression of validated scalability beyond 10⁵.

---

## 4. Clarity & Structure

**Rating: 3 (Adequate)**

The paper is generally well-organized, with a clear roadmap at the beginning of Section IV and consistent notation throughout. The extensive use of tables for parameter documentation (Tables III, IV, V, VI) supports reproducibility. The distinction between protocol overhead η and total channel utilization is clearly maintained.

However, the paper suffers from several clarity issues:

**Excessive length and redundancy.** At approximately 12,000 words (estimated from the LaTeX source), the paper is substantially longer than typical IEEE T-AES articles. There is significant redundancy: the coordinator bandwidth requirement is discussed in Sections III-E, III-F, and IV-A; the traffic accounting appears in Tables II, IV, VI, and the bandwidth breakdown in Table VII; the exception-based telemetry is introduced in Section IV-B and validated in Section IV-E-D. A more disciplined structure could reduce length by 25–30% without losing content.

**The notation is inconsistent in places.** The paper uses both $\eta$ and $\eta_{\text{proto}}$ for protocol overhead (abstract vs. body), $O_{\text{protocol}}$ (Section III-E) and $\eta$ interchangeably, and $C_{\text{node}}$ and $C_{\text{coord}}$ for different bandwidth parameters that could be confused. The footnote system in tables (using superscript letters a, b, c) is overloaded—Table III has footnotes a and c but no b.

**The figures are referenced but not provided** (understandable for a LaTeX submission, but the captions suggest some figures may be analytically generated rather than DES outputs). Fig. 8's caption explicitly notes the 10⁶ curve is extrapolated, which is good practice, but the paper should clarify which other figures show DES results vs. analytical curves.

**The abstract is dense but accurate.** It correctly summarizes the three main contributions and the design envelope. However, the phrase "cycle-aggregated discrete event simulation (DES) with byte-level traffic accounting" is jargon-heavy for the opening sentence.

---

## 5. Ethical Compliance

**Rating: 4 (Good)**

The paper includes a transparent acknowledgment of AI-assisted methodology in the Acknowledgment section, citing specific AI models (Claude 4.6, Gemini 3 Pro, GPT-5.2) and clarifying that the AI-generated concepts are "not validated in the current study." This level of disclosure exceeds current IEEE requirements and is commendable.

The data availability statement is thorough, providing repository URLs, version tags, and software environment specifications. The anonymous authorship ("Project Dyson Research Team") with a note about final publication is acceptable for review but must be resolved before publication per IEEE policy.

One concern: the reference to "Claude 4.6," "Gemini 3 Pro," and "GPT-5.2" in the Acknowledgment section cites model versions that do not exist as of mid-2025. If these are speculative future versions, this should be clarified; if the paper is set in a future timeframe, this is unusual for a technical manuscript and may confuse readers. Similarly, the Starlink reference notes "accessed February 2026," suggesting the paper is written from a future perspective, which is unconventional.

---

## 6. Scope & Referencing

**Rating: 3 (Adequate)**

The paper is appropriate for IEEE T-AES in terms of topic (autonomous spacecraft coordination), though the heavy emphasis on communication protocol overhead analysis might also fit IEEE Transactions on Communications or IEEE Journal on Selected Areas in Communications. The space systems context is maintained throughout, which anchors the work in the T-AES scope.

The reference list is comprehensive (50 references) and covers the relevant literature in constellation management, swarm robotics, distributed systems, and queueing theory. Key foundational works are cited (Lynch, Kleinrock, Lamport, Demers). The inclusion of recent work on GNN-based controllers (Tolstaya, Li) and mean-field games (Lasry, Huang) demonstrates awareness of modern approaches.

However, several gaps exist:

- **No references to DTN/delay-tolerant networking simulation studies** that have addressed similar scale challenges in space networks. The Cerf DTN reference is the architecture RFC, not simulation work.
- **No references to actual ISL link budget analyses** for LEO constellations. The 1 kbps budget is motivated qualitatively but not grounded in published link budget calculations.
- **Missing references to recent mega-constellation coordination work** post-2020, particularly from the Starlink V2 and Kuiper operational literature.
- **The self-citation [dyson_multimodel]** is to a companion paper at a non-archival URL, which weakens the reference chain. If this methodology paper is not peer-reviewed, it should be noted.
- Several references are non-archival (SpaceX website, Amazon website, DARPA program pages, DoD fact sheets). While understandable for operational programs, the paper relies on these for key claims about current constellation scale.

---

## Major Issues

1. **The DES adds minimal value beyond analytical predictions.** The <0.1% agreement between DES and closed-form results across all fleet sizes (Table VIII) demonstrates that the simulation is essentially computing the same arithmetic as the analytical model. The three "DES-unique" contributions (burstiness, AoI, GE losses) are each derivable analytically in a few lines. The paper should either (a) demonstrate DES results that genuinely diverge from analytical predictions (e.g., under correlated failures, dynamic cluster reassignment, or realistic orbital geometry), or (b) reframe the contribution as an analytical design-space characterization with DES verification, rather than claiming the DES produces "results inaccessible to closed-form analysis."

2. **The architecture comparison is not apples-to-apples.** The hierarchical architecture provides coordinator-mediated state awareness; the sectorized mesh provides direct peer monitoring. These offer different coordination capabilities (Table II), yet the overhead comparison treats them as equivalent. The paper needs either (a) a coordination quality metric that normalizes for state awareness differences, or (b) an explicit acknowledgment that the 1.4–1.5× overhead ratio compares architectures with different functional capabilities.

3. **Physical-layer abstraction gap is too large for quantitative claims.** The paper reports specific thresholds (50 kbps, 24 kbps, 21 kbps) and overhead percentages (46%, 65%) to three significant figures, but the MAC efficiency uncertainty (γ ∈ [0.7, 0.9]) introduces ±30% error. The effective overhead range of 51–66% (Table VIII) spans 15 percentage points. Reporting η = 46.0% with SD < 0.001% creates a false impression of precision when the engineering-relevant uncertainty is dominated by unmodeled physical-layer effects.

4. **The latency results in Table VII appear discretized.** Only two latency values appear across seven cluster sizes at $N = 10^5$ (508 ms and 675 ms). This step-function behavior is physically implausible—varying $k_c$ from 50 to 500 should produce a continuous change in regional coordinator queueing delay. This suggests either a simulation artifact (e.g., integer rounding in the queueing model) or an insufficiently resolved timing model. The authors should investigate and explain this discretization.

5. **The paper lacks any validation against real operational data.** Even a rough comparison of the model's predictions against published Starlink or Iridium coordination overhead would substantially strengthen the work. For example, the centralized model at $N = 7,000$ should produce predictions comparable to (or at least consistent with) known Starlink ground station processing loads.

---

## Minor Issues

1. **Abstract, line 1:** "cycle-aggregated discrete event simulation (DES) with byte-level traffic accounting" is jargon-heavy for an opening. Consider leading with the problem statement.

2. **Section I-A:** "one of the significant open challenges" → "a significant open challenge" (more direct).

3. **Table III footnote:** Footnote markers jump from (a) to (c), skipping (b). The (c) marker appears in the table body but the footnote text uses superscript c.

4. **Eq. (4):** $M_{\text{total}}$ counts only uplink messages but is labeled "total." Consider renaming to $M_{\text{up}}$ or clarifying in the equation label.

5. **Section III-C-3, mesh convergence:** The convergence formula $R_{\text{conv}} = \max(\lceil\log_2 N\rceil, \lceil N/(bf)\rceil)$ conflates two different bottlenecks (epidemic spread vs. throughput). The max operation is correct but deserves a sentence of explanation for readers unfamiliar with gossip protocols.

6. **Table I (M/D/c sensitivity):** The "Representative System" column is speculative (e.g., "Hyperscale data center" for $c = 1000$). Consider removing or labeling as illustrative.

7. **Section III-E:** The sentence "the control plane should be sized for the stress case but will operate at <10% utilization during routine operations" appears in both Section IV-D and Section VI. Remove one instance.

8. **Table IX (AoI results):** The "Periodic baseline" row appears twice (as the first row and as $p_{\text{exc}} = 1.0$). Remove the duplicate.

9. **Section IV-C:** "retransmission recovers only ~27% of burst-lost messages" — clarify this is the recovery rate during bad-state bursts specifically, not the overall recovery rate across both states.

10. **Eq. (12):** $C_{\text{raw}} = C_{\text{coord}} / \gamma$ appears orphaned after the TDMA discussion without context. Integrate it into the preceding paragraph.

11. **Section V-A, item 3:** "to ground the MAC efficiency γ assumption" — the verb "ground" is ambiguous (could mean "justify" or "reduce to zero"). Rephrase.

12. **References:** [1] and [3] are non-archival web pages. Per IEEE style, these should be marked as such and include access dates (which they do, but inconsistently—some say "accessed February 2026").

13. **The paper mentions "Claude 4.6," "Gemini 3 Pro," and "GPT-5.2"** — these model versions do not exist as of the review date. Clarify whether these are hypothetical or if the paper is set in a speculative future timeframe.

---

## Overall Recommendation

**Major Revision**

The paper addresses an important problem and provides a well-documented parametric design-space characterization for hierarchical coordination of large space swarms. The transparency about assumptions, limitations, and baseline interpretation is commendable and above average for the field. However, the contribution is undermined by four issues that require substantial revision: (1) the DES adds minimal value beyond analytical predictions, requiring either more complex scenarios that genuinely need simulation or an honest reframing of the contribution; (2) the architecture comparison is not functionally equivalent, making the overhead ratios difficult to interpret; (3) the physical-layer abstraction gap is too large for the quantitative precision claimed; and (4) the lack of any validation against real operational data limits the paper's practical relevance. A major revision addressing these issues—particularly adding scenarios where the DES diverges from analytical predictions and providing at least one real-world validation point—would make this a solid contribution to the T-AES literature.

---

## Constructive Suggestions

1. **Add dynamic scenarios that genuinely require simulation.** The current DES confirms analytical predictions because the message model is nearly deterministic. Introduce scenarios with dynamic cluster reassignment (nodes migrating between clusters due to orbital drift), cascading coordinator failures (correlated events affecting multiple clusters), or adaptive exception thresholds (where $p_{\text{exc}}$ varies based on local conjunction density). These would produce emergent behaviors that analytical models cannot easily predict and would justify the DES methodology.

2. **Validate against a packet-level simulator for one configuration.** Even a single NS-3 or OMNeT++ simulation of one 100-node cluster with realistic optical ISL parameters would ground the MAC efficiency assumption and dramatically strengthen the paper. This would replace the speculative γ ∈ [0.7, 0.9] range with a measured value and provide confidence that the message-layer abstraction is valid.

3. **Develop a coordination quality metric that normalizes across architectures.** Define a metric such as "conjunction detection probability as a function of state staleness" or "fraction of close approaches detected within X seconds" that can be evaluated for both hierarchical (coordinator-mediated) and sectorized mesh (direct peer monitoring) architectures. This would make the overhead comparison meaningful by establishing whether the architectures provide equivalent safety guarantees.

4. **Reduce paper length by 25% through consolidation.** Merge the redundant traffic accounting discussions (currently spread across Tables II, IV, VI, VII and Sections III-E, III-F, IV-E). Present the coordinator bandwidth analysis once (Section IV-A) rather than introducing it in Section III-E and revisiting it. Move the detailed sectorized mesh parameterization (Table IV, neighbor-cap sweep) to an appendix or supplementary material.

5. **Add a real-world calibration point.** Use published data on Starlink conjunction avoidance operations (ESA's annual space environment report, already cited as [50]) to calibrate the centralized model at $N ≈ 7,000$. Even an order-of-magnitude comparison would anchor the simulation in operational reality and demonstrate that the model produces physically meaningful predictions.