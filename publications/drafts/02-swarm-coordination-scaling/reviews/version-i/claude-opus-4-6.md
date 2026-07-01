---
paper: "02-swarm-coordination-scaling"
version: "i"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-23"
recommendation: "Major Revision"
---



# Peer Review: "Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study"

## IEEE Transactions on Aerospace and Electronic Systems

---

## 1. Significance & Novelty

**Rating: 3 (Adequate)**

The paper addresses a genuinely important problem: how coordination architectures scale for very large autonomous spacecraft fleets in the $10^3$–$10^5$ range. The motivation is timely given Starlink's growth trajectory and planned mega-constellations. The authors correctly identify a gap between swarm robotics literature (tens to hundreds of agents) and operational constellation management (~10,000 nodes), and the intermediate regime of $10^4$–$10^5$ is indeed underexplored.

However, the novelty is limited. The central result—that a hierarchical tree with fixed fan-out achieves $O(1)$ overhead percentage scaling—is analytically obvious from the message model (Eq. 5): total messages are $O(N)$, total bandwidth is $O(N)$, so the ratio is $O(1)$. The authors acknowledge this ("The $O(1)$ overhead scaling follows directly from the analytical message model," Section IV-D), which raises the question of what the DES adds beyond confirming a straightforward analytical prediction. The DES essentially validates that $N/N = \text{const}$, which is not a surprising or deep result. The more interesting contributions—exception-based telemetry, coordinator bandwidth parameterization, and link availability analysis—are relatively thin extensions (Bernoulli thinning, simple capacity thresholding, and geometric retry probability) that do not require DES to derive.

The comparison framework is weakened by the authors' own admission that the baselines are "intentional bounds, not realistic competitors" (Section I-C). While this is intellectually honest, it substantially reduces the practical significance of the comparison. The paper would be far more impactful if it included the sectorized mesh variant (acknowledged as future work in Section V-C) or compared against published coordination protocols from the constellation management literature.

---

## 2. Methodological Soundness

**Rating: 2 (Needs Improvement)**

There are several significant methodological concerns:

**Node sampling and extrapolation.** Section III-E states that the simulation uses node sampling with $r_s = \min(1, 1000/N)$, meaning that for $N = 10^5$, only 1% of nodes are actually simulated, with "fleet-wide metrics extrapolated by $1/r_s$." This is a critical design choice that is insufficiently justified. The constant overhead result (Table VII) may be an artifact of this linear extrapolation rather than a genuine emergent property of the DES. If only 1,000 nodes are ever simulated regardless of $N$, and results are simply scaled by $N/1000$, then the "DES-measured" overhead is effectively an analytical calculation dressed up as simulation output. The authors must demonstrate that the sampling does not introduce systematic bias—for instance, by running at least one configuration at $N = 10^5$ with full node simulation and comparing against the sampled result.

**Wall-clock runtime.** The reported runtimes (0.2s for $N=10^3$ to 15s for $N=10^5$, per run) are suspiciously fast for a year-long DES with $10^5$ nodes generating events every 10 seconds. A back-of-envelope calculation: $10^5$ nodes × $0.1$ msg/s × $3.15 \times 10^7$ s/year = $3.15 \times 10^{11}$ events. Even with sampling ($r_s = 0.01$), this is $3.15 \times 10^9$ events—far too many to process in 15 seconds. This suggests either the simulation is far more abstract than described, or the event model is significantly simplified beyond what is stated. The authors should provide a detailed computational complexity analysis of their DES implementation.

**Monte Carlo sample size.** Table VII footnote states "2–5 Monte Carlo runs per configuration" for the main scaling results, despite Section III-D specifying "50–100 independent runs per configuration." This discrepancy is concerning. With only 2–5 runs, the reported standard deviation of "<0.5%" is not statistically meaningful—it likely reflects the deterministic nature of the sampled simulation rather than genuine stochastic variability. The 95% confidence intervals claimed elsewhere cannot be reliably computed from 2–5 samples.

**Queueing model mismatch.** The centralized baseline uses an $M/D/1$ model, but the arrival process is not Poisson: all $N$ nodes report at rate $r = 0.1$ msg/s with a coordination cycle of $T_c = 10$s, which is closer to a deterministic or near-synchronous arrival pattern (especially if nodes are synchronized to the coordination cycle). A $D/D/1$ or $D/D/c$ model would be more appropriate, and the $M/D/1$ assumption inflates the variance and tail latency of the centralized baseline.

**Exception-based telemetry validation.** The "validation" in Table VI confirms that a Bernoulli($p$) process produces approximately $p \times N$ events—this is a verification of the random number generator, not a meaningful validation of exception-based telemetry as a coordination mechanism. A real validation would model state prediction accuracy, threshold selection, and the impact of missed reports on coordination quality (e.g., collision avoidance degradation when nodes fail to report deviating trajectories).

---

## 3. Validity & Logic

**Rating: 2 (Needs Improvement)**

**Circular reasoning in the central result.** The paper's headline finding—$O(1)$ overhead percentage scaling—is a direct mathematical consequence of the model definition, not an empirical discovery. The hierarchical model generates $O(N)$ total messages (Eq. 5), the bandwidth budget is $O(N)$ (each of $N$ nodes has 1 kbps), so $\eta = O(N)/O(N) = O(1)$. The DES "confirms" this by construction. The authors partially acknowledge this but still present it as the "central scalability result" (Section IV-D), which overstates its significance.

**Inconsistency between Tables V and VII.** Table V (cluster size optimization) reports hierarchical overhead of 2.9% at $N = 10^5$ with $k_c = 100$, while Table VII reports 21.5% at the same $N$ and $k_c$. The text notes these use different accounting (Table V uses "optimized varying cluster size" vs. Table VII uses "fixed $k_c = 100$"), but this explanation is insufficient—both tables claim $k_c = 100$ at $N = 10^5$. The discrepancy of 7× needs explicit reconciliation. One possibility is that Table V reports only protocol overhead beyond baseline telemetry while Table VII includes baseline telemetry, but the column headers both say "protocol overhead." This confusion undermines confidence in the quantitative results.

**Coordinator bandwidth assumption.** The paper resolves the coordinator bandwidth bottleneck (20.5 kbps inbound vs. 1 kbps allocation) by assuming coordinators "use the combined coordination bandwidth of [their] cluster" (Section III-F). While Section IV-G parameterizes this, the main results (Tables V and VII) assume full bandwidth pooling ($\beta = 1.0$). This is a strong assumption that requires the coordinator to have a physically different radio or antenna system, which contradicts the "homogeneous rotating coordinators" model. The paper should present main results at $\beta = 0.25$ (the identified minimum) rather than $\beta = 1.0$.

**Latency results lack detail.** Fig. 2 references $10^6$ nodes, but the simulation only runs to $10^5$. Table V reports latency values (85–440 ms) without explaining their composition (propagation vs. queueing vs. processing). The latency model is underspecified: what propagation distances are assumed? For LEO ISLs at ~1000 km range, one-way propagation is ~3.3 ms, so the 85–440 ms values must be dominated by queueing—but the coordinator utilization is stated as $\rho = 0.05$ at $k_c = 100$, which would produce negligible queueing delay. This inconsistency is unexplained.

**Limitations are well-acknowledged** but collectively severe. The abstraction of MAC-layer effects, pointing constraints, orbital mechanics, correlated failures, and the Bernoulli link model (vs. deterministic occlusion) means the quantitative results may not transfer to real systems. The paper would benefit from a clearer statement of which results are robust to these simplifications (qualitative topology ranking) and which are not (specific overhead percentages).

---

## 4. Clarity & Structure

**Rating: 4 (Good)**

The paper is generally well-written and logically organized. The progression from problem statement through simulation framework to results and discussion follows a clear arc. The explicit "Baseline Interpretation Note" (Section I-C) is commendable and should be standard practice for papers comparing against intentionally weak baselines.

Tables are numerous and generally well-formatted, though the proliferation of tables (10 tables) sometimes obscures the narrative. The traffic accounting table (Table IV) and bandwidth breakdown (Table III) are particularly useful for reproducibility. The metric definitions in Section III-G are clear and precise.

However, several clarity issues exist. The paper references "Versions A–G" and "Version H" multiple times (Sections III-F-1, IV-D), which is unusual for a journal submission and suggests the paper has undergone extensive revision history that should be cleaned up for publication—reviewers should not need to know about prior internal versions. The abstract is excessively long (over 300 words) and reads more like an executive summary; it should be condensed to focus on the key finding and its significance. The paper at ~12,000 words (estimated from LaTeX source) is at the upper end of IEEE TAES length limits and could benefit from tightening, particularly in the simulation framework section which repeats information across subsections.

Figures are referenced but not viewable in this review (PDF figures). The figure captions are descriptive and informative, which is good practice. The caption for Fig. 1 references "10–100 regional coordinators" and "10–100 cluster coordinators," but the text consistently uses $k_c = 100$ and $k_r = 100$—the variable ranges in the caption may confuse readers.

---

## 5. Ethical Compliance

**Rating: 4 (Good)**

The paper includes an appropriate disclosure of AI-assisted methodology in the Acknowledgment section, noting that "Claude 4.6 (Anthropic), Gemini 3 Pro (Google DeepMind), and GPT-5.2 (OpenAI)" were used for "exploratory AI-assisted ideation." The disclosure is specific about which models were used and what role they played (architectural concept generation, not analysis or writing). The statement that the AI-generated concept "is not validated in the current study" is appropriately cautious.

The author block uses a team name ("Project Dyson Research Team") with a note that individual names will be provided for final publication. While this is acceptable for initial submission, IEEE policy requires named authors, and the note should be resolved before acceptance. The data availability statement promises open-source code with a pending commit hash, which is good practice but should be finalized.

One concern: the references to future AI model versions (Claude 4.6, GPT-5.2) that do not exist as of mid-2025 suggest either the paper is set in a near-future context or these are placeholder names. This should be clarified to avoid confusion about the actual tools used.

---

## 6. Scope & Referencing

**Rating: 3 (Adequate)**

The paper is broadly appropriate for IEEE TAES, which publishes work on space systems, autonomous systems, and communication architectures. However, the paper's contribution is more aligned with a communications or distributed systems venue (e.g., IEEE TCOM, IEEE TPDS) than an aerospace-specific journal, as the space domain serves primarily as motivation rather than driving the technical analysis. The orbital mechanics, space environment effects, and mission-specific constraints that would make this distinctly an aerospace contribution are largely abstracted away.

The reference list is extensive (48 references) and covers the relevant literature in constellation management, swarm robotics, distributed systems, and queueing theory. Key works are cited: Brambilla et al. [8] for swarm robotics, Lynch [7] for distributed algorithms, Kleinrock [25] for queueing theory, and Demers et al. [26] for gossip protocols. The inclusion of operational references (Starlink, Kuiper, OneWeb, DARPA programs) provides useful context.

Notable omissions include: (1) recent work on distributed satellite autonomy by Nag et al. and others in the IEEE Aerospace Conference proceedings; (2) the substantial literature on cluster-based routing in mobile ad hoc networks (MANETs), which directly addresses hierarchical coordination with rotating cluster heads—this is essentially the same problem in a different domain, and the MANET literature (e.g., LEACH, HEED, weighted clustering algorithms) should be discussed; (3) work on software-defined networking for satellite constellations, which represents a practical middle ground between centralized and fully distributed coordination; and (4) the DTN/CGR (Contact Graph Routing) literature beyond the RFC citation, which addresses scheduled intermittent connectivity in space networks. Several references are non-archival (websites, press releases) and should be supplemented with peer-reviewed sources where possible.

---

## Major Issues

1. **Node sampling invalidates "DES-measured" claims.** The simulation samples only $\min(1, 1000/N)$ of nodes and extrapolates linearly. For $N \geq 10^4$, this means the "DES" is simulating 1,000 nodes and multiplying by a constant. The constant-overhead result is therefore a mathematical tautology, not an empirical finding. The authors must either (a) run full-scale simulations for at least a subset of configurations to validate the sampling approach, or (b) reframe the contribution as analytical with DES spot-checks, rather than claiming DES measurement across two orders of magnitude.

2. **Inconsistency between Tables V and VII.** Both tables report hierarchical overhead at $N = 10^5$ with $k_c = 100$, but values differ by 7× (2.9% vs. 21.5%). The footnote explanation is insufficient. This must be fully reconciled with explicit accounting of what is included/excluded in each table's overhead metric.

3. **Monte Carlo sample sizes are inadequate for main results.** Table VII uses 2–5 runs per configuration despite the methodology section specifying 50–100. Statistical claims (standard deviation <0.5%, 95% CIs) are not credible with 2–5 samples. Either run the specified number of replications or remove statistical precision claims.

4. **The central result ($O(1)$ overhead scaling) is analytically trivial.** The paper needs to reframe its contribution. If the DES adds nothing beyond confirming $N/N = \text{const}$, the value proposition must come from other aspects: the coordinator bandwidth parameterization, link availability analysis, or cluster size optimization. These should be elevated as primary contributions rather than supporting results.

5. **Absence of realistic decentralized comparator.** The global-state mesh is acknowledged as an intentional upper bound, but without a sectorized mesh or other practical decentralized alternative, the paper cannot make meaningful claims about the relative merit of hierarchical coordination. The sectorized mesh described in Section V-C should be implemented and included.

---

## Minor Issues

1. **Abstract length.** At ~350 words, the abstract exceeds typical IEEE TAES guidelines (~200 words). It should be condensed significantly.

2. **Version references.** References to "Versions A–G" and "Version H" (Sections III-F-1, IV-D) should be removed; these are internal revision artifacts inappropriate for a journal submission.

3. **Future AI model names.** The Acknowledgment references "Claude 4.6," "Gemini 3 Pro," and "GPT-5.2," which appear to be fictional future versions. Clarify or correct.

4. **Eq. 2 notation.** The $M/D/1$ waiting time formula $W_q = \rho / [2\mu(1-\rho)]$ is correct for the Pollaczek-Khinchine result with deterministic service, but should cite the specific result (e.g., Kleinrock Vol. 1, Ch. 3) rather than the general reference.

5. **Fig. 2 caption.** References $10^6$ nodes, but the simulation only extends to $10^5$. Either the figure includes extrapolated data (which should be clearly marked) or the caption is incorrect.

6. **Table I.** The "Representative System" column for $c = 1000$ ("Hyperscale data center") is speculative and not representative of any existing space operations infrastructure.

7. **Section III-B-3.** The claim that $D = O(N^{1/3})$ for a random geometric graph in 3D orbital space is incorrect for LEO constellations, which occupy thin spherical shells (effectively 2D), giving $D = O(N^{1/2})$.

8. **Collision avoidance rate.** The $10^{-4}$/node/s rate is well-justified in the text, but the sensitivity analysis (varying from $10^{-5}$ to $10^{-3}$) should be presented in a table rather than inline text.

9. **Eq. 6 and surrounding text.** The power overhead calculation ($\Delta P_{\text{avg}} = 0.15$ W) assumes uniform rotation, but the duty cycle analysis (Table VI) shows rotation periods of 1h–7d, which would produce different time-averaged power depending on the cycle.

10. **Reference [10] (Reynolds 1987)** is cited in the bibliography but never referenced in the text.

11. **Typographical.** Section III-B-2: "fan-out ratio" should be consistent (hyphenated or not) throughout.

---

## Overall Recommendation

**Major Revision**

The paper addresses a relevant problem and is generally well-written, but suffers from a fundamental methodological concern: the node sampling strategy means the "DES-measured" results may be analytically predetermined rather than emergent simulation outputs. The central finding ($O(1)$ overhead scaling) is analytically obvious and the DES does not add meaningful empirical content beyond this prediction. The inconsistency between Tables V and VII, inadequate Monte Carlo sample sizes for the main results, and absence of a realistic decentralized comparator further weaken the contribution. A major revision should: (1) validate the sampling approach against full-scale runs; (2) reconcile all quantitative inconsistencies; (3) reframe the contribution around the more novel elements (coordinator bandwidth, link availability, cluster optimization); (4) implement the sectorized mesh comparator; and (5) run adequate Monte Carlo replications. With these changes, the paper could make a solid contribution to the literature on scalable coordination architectures for mega-constellations.

---

## Constructive Suggestions

1. **Implement and simulate the sectorized mesh variant.** This is described in detail in Section V-C and would transform the paper from a comparison against strawman baselines into a meaningful architectural trade study. Even a simplified sectorized mesh with 2–3 parameterizations would dramatically strengthen the contribution.

2. **Validate the node sampling approach.** Run at least 3 configurations ($N \in \{10^3, 10^4, 10^5\}$) with full node simulation (no sampling) and compare against sampled results. If the results match, the sampling is validated; if not, the main results need revision. Report the comparison explicitly.

3. **Reframe the primary contribution.** The $O(1)$ overhead scaling is not surprising; the more valuable contributions are the coordinator bandwidth parameterization (Section IV-G), the link availability/retransmission analysis (Section IV-F), and the cluster size optimization (Section IV-B). Restructure the paper to lead with these practical design insights rather than the scaling property.

4. **Add a MANET cluster-head literature comparison.** The hierarchical coordination with rotating cluster heads is well-studied in the MANET literature (LEACH, HEED, etc.). A discussion of how the space swarm problem differs from (or is analogous to) terrestrial MANET clustering would strengthen the related work and help readers assess the novelty.

5. **Model coordination quality degradation.** Currently, the paper measures only overhead and message delivery rate. Adding a coordination quality metric—such as the fraction of conjunction events detected within the decision window, or the staleness of fleet state information—would provide a much more meaningful basis for comparing architectures and would justify the DES approach over pure analysis.