---
paper: "02-swarm-coordination-scaling"
version: "bt"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-27"
recommendation: "Major Revision"
---

# Peer Review: "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms"

**Manuscript Version:** BT
**Venue:** IEEE Transactions on Aerospace and Electronic Systems

---

## 1. Significance & Novelty

**Rating: 3 (Adequate)**

The paper addresses a genuine gap: there is no published work providing closed-form parametric sizing equations for hierarchical coordination architectures at the $10^3$–$10^5$ node scale with byte-level traffic accounting. The three-layer feasibility decomposition (byte budget, MAC efficiency, TDMA airtime) is a useful conceptual framework that practitioners could apply. The identification that architecture-specific overhead ($\eta_0 \approx 5\%$) is small while command traffic dominates is a clean and actionable finding.

However, the novelty is somewhat limited by the simplicity of the underlying models. The closed-form equations are essentially deterministic byte-counting exercises (e.g., $\eta_{\text{cmd}} = p_{\text{cmd}} \times S_{\text{cmd}} \times 8 / (C_{\text{node}} \times T_c)$), and the DES confirms these to $<0.1\%$—which is expected given that both operate at the same abstraction level. The paper acknowledges this (Section V-A), but it raises the question of what the DES actually contributes beyond the inter-cycle GE recovery tail statistics. The AoI result (Eq. 12) is a direct application of the geometric distribution CDF, and the coordinator ingress sizing is a straightforward throughput calculation. The intellectual contribution is more in the systematic assembly and parameterization of these relationships than in any individual analytical result.

The paper would be significantly strengthened if the design equations were validated against even one physical-layer scenario. As written, the contribution is a message-layer accounting framework—useful, but the distance from operational relevance is large. The authors are transparent about this gap, which is commendable, but it limits the impact for a T-AES audience that expects some connection to implementable systems.

## 2. Methodological Soundness

**Rating: 3 (Adequate)**

The methodology is internally consistent and clearly documented. The parameter choices are stated explicitly (Table III), the Monte Carlo configuration is reproducible (30 replications, sequential seeds, open-source code), and the analytical cross-checks are thorough. The three-layer feasibility framework is well-structured.

**Strengths:** The TDMA superframe time budget (Table V) is a genuinely useful engineering artifact. The GE parameter sensitivity sweep (Fig. 5b) with DES validation points provides design curves that practitioners could use. The explicit treatment of half-duplex TX/RX partitioning and the unicast stagger formula (Eq. 7) reveal a real constraint that would be missed by byte-budget analysis alone.

**Concerns:** (1) The DES uses a fluid-server ingress model while the analytical results assume TDMA slot scheduling—these are fundamentally different service disciplines. The paper acknowledges this (Section IV-D, model enforcement note) but then draws conclusions about joint parameter interactions from the fluid-server DES that may not hold under TDMA. The statement that "GE losses and coordinator queue occupancy are independent" (Section IV-D) is only true under the fluid-server model; under TDMA, corrupted packets consume slot time, as the authors note—but the DES does not capture this interaction. (2) The 30 MC replications produce SD $< 0.001\%$ for overhead, which is unsurprising given that overhead is deterministic at the message layer. The replications are only meaningful for the GE recovery tails, where 30 runs may be insufficient for P99 statistics (each run at $N=10^4$, $k_c=100$ produces $\sim 3.15 \times 10^6$ AoI samples, but the number of GE loss-streak events is much smaller). (3) The $\sqrt{N}$ sector sizing is described as an "order-of-magnitude heuristic" (Section III-B.4), but the overhead comparison between hierarchical and sectorized mesh depends sensitively on this choice. The "14× bandwidth efficiency per unit of awareness" claim (Section IV-G) is a ratio of two heuristic quantities and should be presented more cautiously.

The static topology assumption is reasonable for co-planar formations but the quantitative bound on re-association overhead ($<0.5\%$, Section V-B) assumes a specific $\lambda_h$ that is not validated against any orbital mechanics model. For cross-plane LEO constellations (the most relevant operational case), cluster membership could change on every orbit, and the transient effects on coordinator state and AoI could be significant.

## 3. Validity & Logic

**Rating: 3 (Adequate)**

The internal logic is sound: the equations are correctly derived, the DES confirms them, and the conclusions follow from the assumptions. The paper is unusually careful about scope claims—repeatedly noting that results are "message-layer predictions" and that physical-layer validation is future work.

**Key validity concerns:**

(1) **Circular validation.** The $<0.1\%$ agreement between DES and closed-form (Table VII) is presented as a primary result, but since both implement the same message-layer model with the same parameters, this is a code verification exercise, not validation. The paper acknowledges this but still lists it as a contribution ("confirms implementation consistency"). This should be reframed as a necessary but insufficient verification step.

(2) **The 1 kbps design point.** The paper argues this is the "design-driving edge case" for RF-backup during optical outages ($<1\%$ of operational time). This is reasonable, but the entire paper's results are dominated by this single parameter choice. At $\geq 10$ kbps, "all message-layer constraints are non-binding" (Table I)—meaning the design equations are only interesting in a narrow operational regime. The paper should more clearly articulate why sizing for a $<1\%$-of-time backup mode justifies the depth of analysis presented.

(3) **Coordinator failure transient analysis.** The triple-fault probability calculation ($1.8 \times 10^{-5}$/yr per cluster) assumes independence between node failure, optical outage, and GE bad-state. The paper notes that these "may be correlated if the failure mode is power-negative or tumbling," but then uses the independence calculation anyway. For a tumbling spacecraft, all three conditions are nearly certain to co-occur, making the independent probability estimate misleading. The RF-backup recovery time of ~160s should be the primary design point without the independence argument.

(4) **Sectorized mesh comparison.** The comparison is structurally unfair: the sectorized mesh is capped at 10 neighbors (3.2% coverage) while the hierarchy provides 100% cluster coverage. The "14× bandwidth efficiency" metric normalizes by peers monitored, but the two architectures provide qualitatively different services. Table IX acknowledges this, but the overhead comparisons in Tables VI and VIII still invite direct comparison. The paper should either compare architectures at equivalent functional scope or more prominently caveat the comparison.

## 4. Clarity & Structure

**Rating: 3 (Adequate)**

The paper is dense but generally well-organized. The roadmap at the beginning of Section IV is helpful. The notation table (Table I) is essential given the number of symbols. The design equations summary in Section V-C is a valuable reference.

**Structural issues:** (1) The paper is very long for a journal article (~12,000 words of body text plus extensive tables and figures). Several sections could be condensed without loss. The sectorized mesh model (Section III-B.4) and its sensitivity analysis (Table IV) consume significant space for what is acknowledged to be a comparator with "narrower service scope." (2) The command dissemination model (Type 1 vs. Type 2) is introduced in Section IV-A but is critical to understanding the stress-case overhead. It should appear earlier, perhaps in the traffic accounting section (III-F). (3) The paper oscillates between presenting results as engineering design tools and as scientific findings. The abstract and introduction frame the work as deriving "closed-form sizing equations," but much of the paper reads as a simulation study. Choosing one framing and committing to it would improve coherence.

**Notation concerns:** $\eta$ is overloaded: it appears as protocol overhead ($\eta_0 + \eta_{\text{cmd}}$), but $\eta_{\text{total}}$ adds the 20.5% baseline, and $\eta_{\text{eff}}$ divides by $\gamma$. While each is defined, the reader must track three related quantities. The subscript convention is inconsistent: $\eta_E$ and $\eta_S$ (workload profiles) vs. $\eta_0$ (architecture-specific) vs. $\eta_{\text{cmd}}$ (command traffic).

**Figures:** All figures are referenced as PDF includes but not provided for review. The captions are detailed and informative, which partially compensates. However, several figures appear to show straightforward linear or constant relationships (e.g., Fig. 8: "Overhead trajectory... $\eta \approx 46\%$ constant across $10^3$–$10^5$"), which may not warrant dedicated figures.

## 5. Ethical Compliance

**Rating: 4 (Good)**

The paper includes an explicit AI-assistance disclosure in the Acknowledgment section, identifying specific models (Claude 4.6, Gemini 3 Pro, GPT-5.2) and their role ("motivated aspects of the coordinator architecture but is not validated here"). This is commendable and exceeds the disclosure practices of most current submissions. The open-source code availability with a specific tag (`paper-02-v-bt`) supports reproducibility.

The anonymous authorship ("Project Dyson Research Team") with a note that "Individual author names and affiliations will be provided for final publication per IEEE policy" is unusual but acceptable for review. The lack of institutional affiliation makes it difficult to assess potential conflicts of interest. The reference to future AI model versions (Claude 4.6, GPT-5.2) suggests the paper may have been written with speculative version numbers, which is mildly concerning for credibility but not an ethical violation.

## 6. Scope & Referencing

**Rating: 3 (Adequate)**

The paper is within scope for T-AES, which publishes work on space systems, autonomous operations, and communication architectures. The references are broad and generally appropriate, covering constellation operations, swarm robotics, distributed systems theory, queueing theory, and AoI. The CCSDS standards references (SPP, Proximity-1, BPv7) ground the message sizes in operational practice.

**Gaps:** (1) The paper does not cite the substantial body of work on satellite network simulation tools (e.g., Hypatia by Kassing et al., 2020; StarPerf by Lai et al., 2020) that address mega-constellation communication modeling at scales relevant to this work. (2) The LEACH comparison (Section II-B) is apt but should also reference more recent cluster-head protocols (HEED, TEEN, PEGASIS) that address the energy-efficiency vs. latency tradeoffs the paper discusses. (3) The AoI framework references are appropriate but miss recent work on AoI in satellite networks specifically (e.g., Yin et al., IEEE TWC 2023; Abd-Elmagid et al., IEEE JSAC 2021). (4) Several references are non-archival (Amazon Kuiper overview, DARPA program pages, DoD fact sheets, McDowell's Space Report). While understandable for operational programs, this weakens the scholarly foundation. (5) Reference [53] (Vallado) and [54] (Alfano) appear in the bibliography but are not cited in the text.

---

## Major Issues

1. **The DES does not validate the analytical results in any meaningful physical sense.** Both the DES and closed-form equations implement identical message-layer assumptions. The $<0.1\%$ agreement is a code verification, not model validation. The paper should either (a) include at least a single-cluster packet-level simulation (even simplified) to bridge the abstraction gap, or (b) substantially reframe the DES contribution as verification-only and reduce the space devoted to DES-vs-analytical comparisons. As written, the repeated emphasis on "$<0.1\%$ agreement" risks misleading readers about the level of validation achieved.

2. **The fluid-server DES and TDMA analytical model are inconsistent.** Table VI (joint interaction) uses fluid-server ingress, but the paper's primary sizing result is TDMA-based (Table V). The claim that "GE losses and coordinator queue occupancy are independent" holds only under fluid-server assumptions. Under TDMA, a corrupted slot is wasted airtime that cannot be reclaimed, creating a coupling between loss rate and effective capacity that the DES does not capture. This inconsistency should be resolved—either by implementing TDMA scheduling in the DES or by clearly restricting the joint-interaction results to the fluid-server regime with explicit caveats about TDMA behavior.

3. **The superframe margin is dangerously thin at the design point.** At 24 kbps with $\gamma = 0.85$, the unallocated margin is 623 ms (6.2% of $T_c$). At $\gamma = 0.80$, it shrinks to 98 ms (0.98%). The paper notes this but still presents 24 kbps as the primary design point. Given that the paper explicitly acknowledges unmodeled overheads (ranging, FEC, control-channel), the 30 kbps "recommended design point" should be promoted to the primary result, and the 24 kbps figure should be presented as the theoretical minimum. The abstract should reflect this.

4. **The topology comparison is structurally unfair and potentially misleading.** The centralized baseline models only compute-queue scalability (not communication), the global-state mesh is an intentional worst case, and the sectorized mesh provides qualitatively different functionality. Only the hierarchical architecture is fully modeled at the communication layer. The paper should either (a) model communication overhead for the centralized baseline (uplink scheduling, ground contact windows) to enable fair comparison, or (b) remove the cross-topology overhead comparison entirely and present the hierarchical results as standalone sizing equations. The current framing—with Table VIII showing hierarchical "between" centralized and mesh—implies a comparison that the methodology does not support.

5. **Uncited references in bibliography.** References [53] (Vallado, *Fundamentals of Astrodynamics*) and [54] (Alfano, conjunction probability) appear in the bibliography but are never cited in the text. These must either be cited or removed per IEEE style requirements.

---

## Minor Issues

1. **Abstract:** "An open-source Monte Carlo tool confirms implementation consistency to $<0.1\%$" overstates the contribution. Suggest: "An open-source Monte Carlo tool verifies the closed-form equations at the message layer to $<0.1\%$."

2. **Section I-C, contribution list:** The enumerated contributions mix architecture-specific findings (items 1, 3) with workload-dependent findings (item 2) and channel modeling (item 4). Consider reorganizing to match the three-layer framework.

3. **Eq. (2), $M/D/1$ waiting time:** The formula $W_q = \rho / (2\mu_s(1-\rho))$ is the Pollaczek-Khinchine result for $M/D/1$, but the standard form is $W_q = \rho / (2\mu(1-\rho))$ where $\mu$ is the service rate. Confirm notation consistency.

4. **Section III-B.2, Eq. (4):** $M_{\text{total}} = N + N/k_c + N/(k_c \cdot k_r)$ counts upward messages only. The bidirectional traffic (commands, heartbeats) is mentioned in the following paragraph but not in the equation. Consider a complete message-count equation or note the omission explicitly.

5. **Table III:** Footnote markers (a, c, d) skip "b." This appears to be a typographical error.

6. **Section IV-A, "Model A" sanity check:** The Monte Carlo estimate of $C_A \approx 50$ kbps from $10^5$ random arrival patterns is stated without confidence intervals or methodology details. This should either be derived analytically (order statistics of uniform arrivals plus deterministic service) or documented with proper statistical reporting.

7. **Section IV-B, Eq. (12):** The ceiling function $\lceil \ln(0.01)/\ln(1-p_{\text{exc}}) \rceil$ gives the number of cycles, but AoI should be multiplied by $T_c$ only if the ceiling is applied after the division. The current notation is correct but could be clearer with parentheses: $T_c \cdot \lceil \ln(0.01)/\ln(1-p_{\text{exc}}) \rceil$.

8. **Table VI, "GE Only" column:** The drops are identical to "No Loss" at every capacity level. This is because GE losses occur before the coordinator queue (as explained in the text), but the column header "GE Only" is misleading—it suggests GE is active but has no effect. Consider renaming to "GE Loss (pre-queue)" or adding a clearer note.

9. **Section III-B.3:** The gossip fanout $f = N/\log_2 N$ is described as "aggressive" but is actually extreme—standard gossip uses $f = O(\log N)$ or even $O(1)$. The choice is justified for single-cycle convergence, but the resulting $O(N^2)$ complexity makes the global-state mesh a straw man rather than a meaningful comparator. Consider also showing $f = \log_2 N$ (standard gossip) with multi-round convergence.

10. **Acknowledgment section:** The AI model versions cited (Claude 4.6, GPT-5.2) do not correspond to any publicly released models as of the review date. If these are internal/beta versions, this should be noted; if speculative, they should be removed.

11. **Section V-B:** "Cluster-boundary crossings occur on ~45–90 min timescales" is stated without derivation. A brief orbital mechanics justification (e.g., relative drift rate for adjacent planes at 550 km altitude) would strengthen this claim.

12. **Table V footnote:** "Under degraded $\gamma = 0.80$: slot duration grows to 98.0 ms, ingress to 9,702 ms, margin shrinks to 98 ms." This means the system has essentially zero margin for any unmodeled overhead. This critical finding is buried in a table footnote and deserves prominence in the main text.

---

## Overall Recommendation

**Major Revision**

The paper addresses a real gap in the literature and provides a systematic, well-documented framework for sizing hierarchical coordination architectures. The three-layer feasibility decomposition, the TDMA superframe budget, and the GE recovery design curves are genuinely useful engineering contributions. However, the paper suffers from four significant issues that prevent acceptance in its current form: (1) the DES-vs-analytical agreement is verification, not validation, but is presented with language suggesting stronger evidential status; (2) the fluid-server DES and TDMA analytical model are inconsistent, undermining the joint-interaction results; (3) the cross-topology comparison is structurally unfair and should be reframed or removed; and (4) the paper is substantially longer than necessary, with several sections (sectorized mesh sensitivity, duty cycle analysis) that could be condensed or moved to supplementary material. A revised version that addresses these issues—particularly by either bridging the message-to-physical-layer gap or more honestly scoping the contribution as a message-layer-only framework—would be a solid contribution to T-AES.

---

## Constructive Suggestions

1. **Implement TDMA slot scheduling in the DES.** The most impactful single improvement would be adding a TDMA-aware service discipline to the DES (even as an option), so that the joint-interaction results (Table VI) and the superframe margin (Table V) can be verified in simulation rather than checked analytically. This would also reveal whether GE losses and TDMA scheduling interact in ways the current fluid-server model misses.

2. **Promote the 30 kbps design point and reframe the 24 kbps result.** The 623 ms margin at 24 kbps is insufficient for operational use given unmodeled overheads. Present 30 kbps as the recommended coordinator PHY rate throughout (abstract, conclusions, design equations summary), with 24 kbps as the theoretical minimum. This is more honest and more useful to practitioners.

3. **Condense the topology comparison to a single table with explicit scope caveats.** Replace the current multi-table, multi-figure comparison with a single table that clearly states what each architecture models (compute-queue only, communication-layer, etc.) and what functional scope it provides. Remove or substantially shorten the sectorized mesh sensitivity analysis (Table IV), which consumes significant space for a comparator acknowledged to have "narrower service scope."

4. **Add a "Practitioner's Quick Reference" box.** The design equations in Section V-C are the paper's most useful output. Consider formatting them as a highlighted box or standalone table with input parameters, equations, and example calculations for 1 kbps, 10 kbps, and 100 kbps regimes. This would make the paper immediately useful to constellation designers.

5. **Scope the contribution more precisely in the abstract and introduction.** Replace claims about "confirming implementation consistency" with "verifying closed-form equations at the message layer." Add a sentence explicitly stating that the contribution is a parametric sizing framework, not a validated system design—and that the value lies in identifying which constraints bind at which bandwidth regimes, enabling focused physical-layer simulation of only the binding cases.