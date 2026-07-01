---
paper: "02-swarm-coordination-scaling"
version: "bp"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-27"
recommendation: "Major Revision"
---



# Peer Review: "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms"

## 1. Significance & Novelty

**Rating: 3 (Adequate)**

The paper addresses a genuine gap: there is no existing work that provides closed-form parametric sizing equations for hierarchical coordination architectures at the $10^3$–$10^5$ node scale with byte-level traffic accounting. The three-layer feasibility decomposition (byte budget, MAC efficiency, TDMA airtime) is a useful conceptual contribution that practitioners could adopt. The identification that architecture-specific overhead ($\eta_0 \approx 5\%$) is small relative to topology-invariant command traffic ($\eta_{\text{cmd}}$ up to 41%) is a genuinely interesting finding—it suggests that debates about coordination topology may be secondary to workload management for bandwidth-constrained systems.

However, the novelty is tempered by the level of abstraction. The "closed-form equations" are essentially straightforward accounting identities (bytes per cycle divided by bandwidth) rather than deep analytical results. Equation (4) for hierarchical message count is elementary combinatorics; Equation (6) for AoI P99 is a standard geometric quantile; the GE recovery analysis is a textbook Markov chain calculation. The intellectual contribution lies more in the systematic assembly and cross-checking of these relationships than in any individual derivation. The paper would benefit from more clearly positioning itself as a *systems engineering sizing framework* rather than implying analytical novelty in the individual equations.

The claimed scale range ($10^3$–$10^5$) is somewhat misleading. The DES validates up to $10^5$, but because $\eta$ is $O(1)$ by construction (fixed $k_c$, linear message scaling), the "validation" at different fleet sizes is essentially confirming that $N$ cancels from the overhead ratio—a mathematical certainty, not an empirical finding. The interesting scaling questions (coordinator failure cascades, inter-cluster routing under dynamic topology, correlated failures across clusters) are explicitly deferred.

## 2. Methodological Soundness

**Rating: 3 (Adequate)**

The methodology is internally consistent but operates at a level of abstraction that limits its practical utility. The cycle-aggregated DES is well-described (Section III-A), and the authors are commendably transparent about what is and is not modeled. The Monte Carlo configuration (30 replications, bootstrap CIs) is appropriate for the message-layer statistics being estimated.

**Strengths:** The three-layer feasibility framework (Table V) is methodologically sound and provides a clear decision procedure. The TDMA superframe budget (Table IV) is a concrete engineering artifact. The GE parameter sensitivity sweep (Fig. 5b) provides genuinely useful design curves. The explicit distinction between fluid-server DES and analytical TDMA checking is honest and well-handled.

**Concerns:** The DES and the closed-form equations operate at *identical* abstraction levels—the DES is essentially a programmatic re-implementation of the same accounting. The $<0.1\%$ agreement (Table VII) therefore confirms code correctness, not model validity, as the authors acknowledge. However, this raises the question: what does the DES add beyond the closed-form equations? The inter-cycle GE recovery statistics (Fig. 5) are the primary DES-specific contribution, but these too match the Markov chain prediction closely. The joint interaction verification (Section IV-D, Table VI) is the strongest justification for the DES, but the finding (GE losses and queue drops are independent under dedicated links) is analytically obvious—lost messages never enter the queue.

The 1 kbps design point is well-motivated as an RF-backup edge case, but the paper spends disproportionate effort analyzing a regime that applies $<1\%$ of operational time. The $\geq$10 kbps regime, where "all constraints are non-binding," receives only a few sentences (Table I, end of Section IV-A). This inverts the practical importance: the interesting engineering questions at 10+ kbps (antenna scheduling, visibility, interference) are exactly the ones deferred.

The static topology assumption is a significant limitation for LEO cross-plane configurations. The quantitative bound ($f_h = 0.8\%$, Section V-B) is helpful but assumes independent re-associations; correlated cluster disruptions (e.g., during orbital plane precession) could be much worse.

## 3. Validity & Logic

**Rating: 3 (Adequate)**

The internal logic is generally sound, and the authors are careful to qualify their claims. The decomposition $\eta = \eta_0 + \eta_{\text{cmd}}$ is valid under the assumed message model, and the finding that $\eta_{\text{cmd}}$ dominates is well-supported. The three workload profiles (Table V) provide a reasonable design envelope.

**Logical concerns:**

1. **Circular validation.** The paper's central claim—that the DES "confirms" the closed-form equations to $<0.1\%$—is presented as a validation result, but since both operate at the same abstraction level, this is implementation verification, not validation. The paper acknowledges this (Section V-A) but still uses language like "confirms" throughout that may mislead readers.

2. **Sectorized mesh comparison fairness.** The comparison between hierarchical ($\eta = 46\%$, 100 peers monitored) and sectorized mesh ($\eta = 65\%$, 10 peers monitored) is presented as a $14\times$ efficiency advantage per peer. However, the sectorized mesh provides a fundamentally different service (local neighborhood monitoring without coordinator dependency). The "cost per peer" metric conflates bandwidth efficiency with functional value—monitoring 100 cluster peers may not be $14\times$ more valuable than monitoring 10 nearest neighbors for conjunction avoidance. Table IX (capability matrix) partially addresses this, but the $14\times$ claim in Section IV-G is misleading without stronger caveats.

3. **Coordinator failure analysis.** The triple-fault probability ($1.8 \times 10^{-5}$/yr per cluster) assumes independence between coordinator failure, optical outage, and GE bad-state. The paper notes that these may be correlated (power-negative or tumbling scenarios) but then uses the independent probability anyway. For a design-driving reliability analysis, the correlated case should be the primary calculation.

4. **The $M/D/1$ centralized model** (Eq. 1–2) uses $\mu_s = 1{,}000$ msg/s, which saturates at $N = 10{,}000$. This is acknowledged as "an intentional compute bound," but the centralized baseline then appears in topology comparisons (Table VIII, Fig. 8) where it diverges—creating a visual impression that centralized coordination fails at $10^4$ nodes, when in practice the binding constraint is propagation latency and spectrum, not processing. The footnotes clarify this, but the figures are misleading at first glance.

## 4. Clarity & Structure

**Rating: 3 (Adequate)**

The paper is dense but generally well-organized. The roadmap at the beginning of Section IV is helpful. The notation table (Table I) is essential given the number of symbols. The design equations summary (Section V-C) is a valuable reference.

**Structural issues:**

1. **Length and repetition.** The paper is extremely long for a journal article. Key results ($\eta \approx 46\%$, coordinator ingress $\approx 24$ kbps, AoI P99 $= 440$ s, GE P95 $= 4$ cycles) are stated in the abstract, introduction, results, discussion, and conclusion—often with identical numerical values. The sectorized mesh model description (Section III-B.4) could be shortened significantly.

2. **Excessive qualification.** Nearly every claim is followed by caveats, footnotes, and cross-references. While intellectual honesty is commendable, the density of qualifications makes it difficult to extract the main message. For example, the command dissemination discussion (Section IV-A) introduces Type 1/Type 2 commands, broadcast vs. unicast, emergency priority, and 22-cycle staggering—all important details, but the presentation buries the key insight (broadcast commands fit; unicast commands don't) under layers of secondary analysis.

3. **Figure quality cannot be assessed** since figures are referenced but not provided. The captions are detailed and informative, which is good practice.

4. **The abstract** is accurate but reads more like a technical summary than an abstract—it includes too many specific numbers (623 ms, 440 s, 4 cycles, $p_{BG} = 0.50$) that are meaningless without context.

## 5. Ethical Compliance

**Rating: 4 (Good)**

The AI-assistance disclosure in the Acknowledgment section is appropriate and specific (Claude 4.6, Gemini 3 Pro, GPT-5.2), with a reference to the methodology paper. The authors clearly state that the AI-assisted ideation "is not validated here," which is an honest framing. The data availability statement provides a specific GitHub repository and tag, enabling reproducibility.

The anonymous authorship ("Project Dyson Research Team") with a note that "Individual author names and affiliations will be provided for final publication per IEEE policy" is acceptable for review but must be resolved before publication. The lack of a conflict-of-interest statement should be addressed.

One minor concern: the reference to future AI model versions (Claude 4.6, GPT-5.2) suggests the paper may be set in a near-future timeframe, which is unusual. If these are actual tools used, the versions should be verified; if speculative, this should be clarified.

## 6. Scope & Referencing

**Rating: 3 (Adequate)**

The paper is appropriate for IEEE TAES in topic (autonomous spacecraft coordination), though the message-layer abstraction may be more suited to a communications or systems engineering venue. The reference list is comprehensive (50+ references) and covers the relevant domains: constellation operations, swarm robotics, distributed systems theory, AoI, and CCSDS standards.

**Referencing concerns:**

1. Several references are non-archival (Amazon Kuiper overview, DARPA program pages, DoD fact sheets, NRL magazine article). While understandable for operational programs, these weaken the scholarly foundation. The Starlink reference (FCC filing + non-archival blog) should be supplemented with peer-reviewed analyses.

2. The LEACH reference [heinzelman_leach] is appropriate for cluster-head rotation but is from 2000; more recent WSN clustering work (e.g., HEED, TEEN, or survey papers from 2015+) would strengthen the connection.

3. The paper cites Castet and Saleh [castet_smallsat_reliability] for the 2%/yr failure rate but this 2009 paper covers early small satellites. More recent reliability data (e.g., from Starlink operational experience or ESA's 2024 space environment report, which is cited but not used for reliability) would be more appropriate for the $10^3$–$10^5$ regime.

4. Missing references: the paper does not cite key works on satellite cluster management (e.g., Schilling's work on formation flying communication), space-based TDMA standards (CCSDS 401.0), or recent mega-constellation autonomy papers from IEEE Aerospace Conference 2023–2024.

---

## Major Issues

1. **The validation claim is overstated.** The $<0.1\%$ DES-to-analytical agreement is implementation verification, not validation. The paper needs either (a) a physical-layer validation component (even a simplified NS-3 single-cluster experiment) or (b) a much more prominent and consistent framing as "message-layer sizing equations pending physical-layer validation." Currently, the framing oscillates between these positions. The title should include "Message-Layer" to set expectations.

2. **The DES contribution is marginal.** If the closed-form equations and the DES produce identical results by construction, the DES adds little beyond code verification. The authors should either (a) introduce physical-layer effects into the DES (even simplified MAC contention) to create a genuine gap between analytical and simulated results, or (b) reframe the paper as purely analytical with the DES as a verification tool, reducing the simulation framework description accordingly.

3. **The topology comparison is not apples-to-apples.** The centralized baseline models only compute queuing; the global-state mesh is an intentional worst case; the sectorized mesh provides different functionality. Only the hierarchical architecture is fully characterized. The paper should either (a) restrict comparisons to hierarchical-only analysis (removing the misleading cross-topology figures) or (b) model all architectures at the same level of fidelity.

4. **The 1 kbps regime receives disproportionate attention.** The paper acknowledges this applies $<1\%$ of operational time but devotes $>90\%$ of the analysis to it. The $\geq$10 kbps regime—where the system actually operates—is dismissed in a few sentences. A more balanced treatment would strengthen the practical contribution.

5. **Intra-cycle ARQ infeasibility (Section IV-A) contradicts the link availability analysis (Table X).** Table X reports $M_r = 2$ retransmission results that "apply to Regime A only ($\geq$10 kbps or $k_c \leq 30$)," but the table header and body do not make this restriction visually clear. A reader could easily apply the $M_r = 2$ delivery rates to the 1 kbps design case, obtaining incorrect results.

---

## Minor Issues

1. **Eq. (1):** The variable $r$ appears without definition in the equation; it is defined later as 0.1 msg/s in Table III but should be introduced at first use.

2. **Section III-B.2:** "The DES models full bidirectional traffic... the reported $\eta \approx 46\%$ includes both directions." It would be helpful to decompose the 46% into uplink and downlink components explicitly.

3. **Table II:** The footnote "a" for AoI states it "depends on $p_{\text{exc}}$ and $T_c$, not $C_{\text{node}}$"—this is only true for the exception-telemetry AoI model. Under full reporting with queue drops (which depend on $C_{\text{node}}$), AoI would vary with bandwidth.

4. **Section III-B.2:** The Raft election description states "quorum $= k_c/2 + 1 = 51$ responders required" but Raft requires a majority of *voting members*, which may differ from $k_c$ if some nodes have failed. Clarify whether failed nodes are excluded from the quorum denominator.

5. **Eq. (7):** The AoI P99 formula uses $\lceil \cdot \rceil$ (ceiling), which is correct for discrete cycles, but the text says "440 s" while the DES gives "441 s." The 1-second difference is within the ceiling function's discretization but should be noted explicitly.

6. **Table VI:** The "GE Only" column is identical to "No Loss" for all capacity levels. The footnote explains this (lost messages never reach the queue), but the column is redundant and could be replaced with a single note.

7. **Section III-B.3:** The gossip fanout $f = N/\log N$ is described as "aggressive" but is actually chosen to guarantee single-cycle convergence. Standard gossip uses $f = O(\log N)$; the distinction should be clearer.

8. **Table III:** Footnote "c" says $\mu_s$ is "set low for single-server bound" but 1,000 msg/s is not obviously "low"—it depends on the processing task. Clarify what realistic processing rates might be.

9. **Section IV-A:** "Fleet-wide TDMA cost is 0.28 kbps/node (1% coordinators at $k_c = 100$)"—this calculation is not shown and the 0.28 kbps figure is unclear. Is this the amortized coordinator PHY rate across all nodes?

10. **Acknowledgment:** "Claude 4.6, Gemini 3 Pro, GPT-5.2" — these version numbers do not correspond to any publicly released models as of mid-2025. Clarify whether these are internal designations or future projections.

---

## Overall Recommendation

**Major Revision**

The paper addresses a legitimate gap in the literature and provides a useful systems engineering framework for sizing hierarchical coordination architectures. The three-layer feasibility decomposition, the design equations summary, and the GE sensitivity curves are genuine contributions. However, the paper suffers from three fundamental issues: (1) the validation claim is overstated—the DES and closed-form equations are tautologically equivalent, and no physical-layer validation is provided; (2) the topology comparisons are not at equivalent fidelity levels, making cross-architecture conclusions unreliable; and (3) the paper is excessively long with significant repetition. A major revision should reframe the contribution as a *message-layer sizing framework* (not a validated coordination architecture), reduce the paper length by ~30%, and either add a minimal physical-layer validation or clearly scope the contribution as analytical-only. The core results are sound and potentially useful to the community, but the current presentation overpromises relative to what is delivered.

---

## Constructive Suggestions

1. **Add a minimal physical-layer validation.** Even a single-cluster NS-3 simulation ($k_c = 100$, TDMA, 24 kbps PHY) with realistic MAC timing would transform this paper. The superframe budget (Table IV) provides the specification. Compare the NS-3 delivery rate and AoI against the message-layer predictions; the *gap* between them is the paper's most important unreported result.

2. **Restructure around the design equations, not the DES.** The paper's lasting contribution is the sizing framework (Section V-C). Make this the centerpiece: present the equations first, then use the DES and analytical cross-checks as verification. This would allow significant compression of Sections III and IV while strengthening the paper's identity.

3. **Provide a worked design example.** Show a practitioner how to use the equations: given a target fleet size, operational tempo, and link budget, walk through the sizing procedure step by step. This would dramatically increase the paper's practical value and is more impactful than additional sensitivity sweeps.

4. **Resolve the topology comparison or remove it.** Either model all architectures at the communication layer (including centralized uplink scheduling) or restrict the paper to hierarchical-only analysis. The current mixed-fidelity comparison invites misinterpretation. If retained, move the centralized and global-mesh baselines to an appendix.

5. **Address the $\geq$10 kbps regime substantively.** Since this is the nominal operating regime, dedicate at least one subsection to identifying which *unmodeled* constraints become binding (antenna scheduling, visibility windows, inter-cluster routing) and provide order-of-magnitude estimates. This would significantly increase the paper's relevance to operational mega-constellation programs.