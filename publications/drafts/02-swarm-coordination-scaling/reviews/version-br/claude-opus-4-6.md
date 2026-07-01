---
paper: "02-swarm-coordination-scaling"
version: "br"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-27"
recommendation: "Major Revision"
---

# Peer Review: "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms"

**Manuscript Version:** BR
**Venue:** IEEE Transactions on Aerospace and Electronic Systems

---

## 1. Significance & Novelty

**Rating: 3 (Adequate)**

The paper addresses a genuine gap: there is no published work providing closed-form parametric sizing relationships for coordination architectures spanning $10^3$–$10^5$ autonomous space nodes with byte-level traffic accounting. The authors correctly identify that swarm robotics literature operates at tens-to-hundreds of agents, constellation management addresses ~$10^4$ nodes without byte-level accounting, and networking literature treats routing without coordination overhead analysis. The three-layer feasibility framework (byte budget, MAC efficiency, TDMA airtime) is a useful conceptual contribution that practitioners could apply.

However, the novelty is tempered by the nature of the results. The core finding—that architecture-specific overhead ($\eta_0 \approx 5\%$) is small while command traffic dominates—is, upon reflection, somewhat predictable from the message model itself. When commands are 512 B and heartbeats are 64 B, and commands are topology-invariant by construction, the dominance of command traffic is an arithmetic consequence of the assumed message sizes rather than an emergent insight. The paper would benefit from more clearly articulating what is *surprising* versus what is a direct consequence of parameter choices. The LEACH literature [Heinzelman et al.] already establishes that aggregation reduces per-node overhead to $O(1)$ in clustered architectures; the contribution here is the specific quantification for space ISL constraints, which is useful but incremental.

The paper's scope is also somewhat narrow for the ambition of its title. "Design Equations" suggests general-purpose tools, but the equations are specific to a particular message model with fixed message sizes, a particular hierarchy depth (four levels), and a particular failure model. The generalizability to alternative coordination semantics (e.g., consensus-based decision-making, distributed optimization) is not addressed.

## 2. Methodological Soundness

**Rating: 3 (Adequate)**

The analytical framework is internally consistent and carefully constructed. The three-layer feasibility decomposition is methodologically sound, and the authors are commendably transparent about what is and is not modeled. The cycle-aggregated DES serves its stated purpose (implementation consistency checking) well, and the $<0.1\%$ agreement with closed-form equations (Table VI) is reassuring—though this tight agreement also raises the question of whether the DES adds independent information beyond confirming arithmetic.

**Strengths:** The GE link model with per-cycle coherence is well-motivated (Section IV-C), and the sensitivity sweep over $p_{BG}$ and $p_B$ (Fig. 5b) provides genuinely useful design curves. The TDMA superframe budget (Table IV) is a concrete, verifiable artifact. The slot-level TDMA simulator provides independent verification of the superframe feasibility, which strengthens the TDMA-related claims.

**Concerns:** The most significant methodological issue is the gap between the fluid-server DES and the TDMA scheduling reality. Table V explicitly states that "TDMA slot scheduling and half-duplex partitioning are *not* enforced in the DES—they are checked analytically." This means the joint interaction results (Section IV-D) are validated only under fluid-server assumptions, not under the actual proposed MAC. The slot-level simulator partially addresses this but only for single-cluster superframe feasibility, not for multi-cluster interactions or contention. The paper acknowledges this (Section V-A), but the gap is significant enough that the "design equations" should be presented with stronger caveats about their domain of validity.

The Monte Carlo configuration (30 replications) is adequate for mean estimation given the low variance reported (SD $< 0.001\%$), but for tail statistics (P99 AoI, maximum GE streaks), 30 replications may be insufficient. The P99 AoI of 441 s is computed over ~$3.15 \times 10^6$ samples per run, which is reasonable, but the maximum observed GE streaks (10–13 cycles) are extreme-value statistics where 30 replications provide limited confidence. The bootstrap CI reported ([438, 444] s) for P99 AoI is reassuringly tight, but similar CIs for maximum statistics would be informative.

The $\sqrt{N}$ sector sizing (Section III-B.4) is described as "an order-of-magnitude heuristic," which is honest but weakens the sectorized mesh as a meaningful comparator. The functional scope difference (Table IX) is well-documented, but the $14\times$ bandwidth efficiency claim (Section IV-G) compares architectures with fundamentally different service levels, which limits its utility.

## 3. Validity & Logic

**Rating: 3 (Adequate)**

The internal logic is generally sound, and the authors are careful to qualify claims. The decomposition $\eta = \eta_0 + \eta_{\text{cmd}}$ is clean and the scale-invariance of $\eta$ across $10^3$–$10^5$ follows directly from the $O(N)$ message count with fixed per-node bandwidth. The AoI analytical cross-check (Eq. 8 vs. DES: 440 s vs. 441 s) is convincing.

**Logical concerns:**

1. **Circular reasoning in the centralized baseline.** The centralized model (Eq. 1–2) sets $\mu_s = 1{,}000$ msg/s to create a processing bottleneck at $N = 10^4$, then uses this bottleneck to argue for hierarchical coordination. But the paper acknowledges this is "an intentional compute bound" and that centralized architectures are "actually limited by propagation latency and uplink spectrum." This makes the centralized baseline a straw man for overhead comparison. The paper partially addresses this by restricting cross-architecture comparisons to hierarchical vs. sectorized mesh, but Figs. 8 and 10 still prominently display the centralized divergence, which could mislead readers.

2. **The 1 kbps design point.** The paper justifies 1 kbps as the "design-driving edge case" for RF backup during optical outages ($<1\%$ of operational time). This is reasonable for survivability analysis, but the paper then derives all primary results at this operating point. The claim that "at $\geq$10 kbps all constraints are non-binding" (Table II) effectively says the design equations are only interesting in a degraded mode that occurs $<1\%$ of the time. This undermines the practical significance of the sizing equations for normal operations.

3. **Coordinator failure transient analysis.** The triple-fault probability ($1.8 \times 10^{-5}$/yr per cluster) assumes independence between coordinator failure, optical outage, and GE bad-state. But the paper itself notes these "may be correlated if the failure mode is power-negative or tumbling." The independence assumption for the probability calculation contradicts the stated correlation concern. The RF-backup recovery time (~160 s) is presented as the "nominal reliability design point," but the analysis of what happens to the cluster during this 16-cycle gap is thin—only stating AoI impact of "+100–200 s."

4. **Static topology assumption.** The quantitative bound on re-association overhead ($f_h = 0.8\%$ of nodes in handoff at any time) is useful, but the claim that "fixed cluster membership is acceptable for bandwidth sizing" because "$\eta$ depends on $k_c$ and message sizes, not node identities" is only true in steady state. During re-association, the transient involves simultaneous membership in two clusters, potential duplicate reports, and coordinator state inconsistency—none of which are captured.

## 4. Clarity & Structure

**Rating: 4 (Good)**

The paper is well-organized and generally well-written. The roadmap at the beginning of Section IV is helpful. The notation table (Table I) is clear, and the consistent use of $\eta_0$ vs. $\eta_{\text{cmd}}$ vs. $\eta_{\text{total}}$ throughout is appreciated. The three-layer feasibility framework (Table VII) is an effective organizing device.

**Strengths:** The paper is unusually transparent about its limitations and modeling boundaries. Phrases like "not modeled," "future work," and "by model construction" appear frequently and appropriately. The superframe time budget (Table IV) is an exemplary presentation of a system-level timing analysis. The design equations summary (Section V-C) is a useful reference.

**Weaknesses:** The paper is dense—perhaps too dense for a journal article. At ~12 pages of technical content (excluding references), it attempts to cover coordinator sizing, AoI, GE recovery, joint interactions, workload profiles, topology comparisons, cluster size sensitivity, duty cycle analysis, and link availability. Some of these (e.g., duty cycle analysis in Table VIII) receive insufficient depth to be convincing and could be deferred to a companion paper. The abstract, while accurate, reads more like an executive summary than an abstract—it includes too many specific numbers (22-cycle staggering, 623 ms margin, 440 s P99) that would be better placed in the conclusions.

The paper occasionally over-qualifies statements to the point of reducing readability. For example, the phrase "topology-invariant *given the assumed workload semantics* (centralized command generation; volume and addressing may differ under alternative decision architectures)" in Section I-C is a parenthetical that should be a footnote or deferred to the discussion.

Figures are referenced but not included in the LaTeX source (only filenames), so I cannot evaluate their quality directly. Based on captions, they appear appropriate and well-described.

## 5. Ethical Compliance

**Rating: 4 (Good)**

The paper includes an explicit acknowledgment of AI-assisted ideation (Claude 4.6, Gemini 3 Pro, GPT-5.2) with a citation to a methodology paper and the appropriate caveat that the AI-motivated architecture "is not validated here." This is commendable transparency. The data availability statement provides a specific repository URL and tag, enabling reproducibility. The anonymous authorship ("Project Dyson Research Team") with a note about final publication is acceptable for review but must be resolved before publication per IEEE policy.

One minor concern: the acknowledgment states AI tools "motivated aspects of the coordinator architecture," but it is unclear which specific aspects. IEEE's policy on AI-assisted writing and research is evolving; the authors should ensure compliance with the current TAES policy at the time of final submission. The use of future software version numbers (Claude 4.6, GPT-5.2) is unusual and may indicate the paper was written with AI assistance beyond what is disclosed, or may simply reflect the authors' projection of tool versions at publication time—this should be clarified.

## 6. Scope & Referencing

**Rating: 3 (Adequate)**

The paper is appropriate for IEEE TAES in its treatment of autonomous spacecraft coordination, though it sits at the boundary between communications/networking and aerospace systems. The reference list (50 entries) is comprehensive and covers the relevant domains: constellation operations, swarm robotics, distributed systems theory, queueing theory, and space communication standards.

**Strengths:** The CCSDS standards references (SPP, Proximity-1, BPv7) ground the message model in real space communication practice. The LEACH reference appropriately acknowledges the WSN heritage of cluster-head rotation. The AoI references (Kaul, Yates, Kadota) are current and authoritative.

**Weaknesses:** Several references are non-archival (Amazon Kuiper overview, DARPA program pages, DoD fact sheets, NRL magazine article) and may not be accessible long-term. While these are appropriately flagged as "non-archival," the paper relies on them for establishing the operational context. More critically, the paper lacks references to several directly relevant bodies of work:

- **Satellite network TDMA scheduling:** The TDMA frame analysis would benefit from references to actual satellite TDMA implementations (e.g., DVB-RCS2, MF-TDMA in military SATCOM).
- **Space network simulation:** No reference to existing space network simulators (e.g., SNS3 for ns-3, or STK/MATLAB-based tools) that could contextualize the custom DES.
- **Cluster-based satellite coordination:** Recent work on distributed satellite systems (e.g., Radhakrishnan et al., "Survey of Inter-Satellite Communication for Small Satellite Systems," IEEE Commun. Surveys Tuts., 2016) is missing.
- **Age of Information in satellite networks:** Recent AoI work specific to satellite systems would strengthen Section IV-B.

---

## Major Issues

1. **Fluid-server vs. TDMA gap undermines joint interaction claims.** The DES uses fluid-server ingress while the paper's primary contribution is TDMA-based sizing. Table V's joint interaction results are therefore validated under a different MAC model than the one proposed. The slot-level TDMA simulator only checks single-cluster superframe feasibility, not multi-cluster or joint GE+capacity interactions under TDMA. This is the paper's most significant methodological gap. **Required action:** Either (a) implement TDMA scheduling in the DES and re-validate Table V, or (b) explicitly restrict all joint interaction claims to the fluid-server model and add a prominent caveat that TDMA joint behavior is unverified.

2. **Limited practical significance at the nominal operating point.** The paper's own analysis shows that at $\geq$10 kbps (the normal operating regime), "all message-layer constraints are non-binding" (Table II). This means the design equations are primarily relevant during RF-backup mode ($<1\%$ of operational time). The paper needs to either (a) more strongly motivate why the degraded-mode sizing is the primary contribution (e.g., by quantifying the operational consequences of coordination loss during optical outages), or (b) extend the analysis to include constraints that *are* binding at higher bandwidths (antenna scheduling, visibility, interference—currently listed as "future work").

3. **Sectorized mesh comparison is not apples-to-apples.** The paper acknowledges the functional scope difference (Table IX) but still makes quantitative overhead comparisons ($1.35$–$1.95\times$ higher, $14\times$ cost per peer). These comparisons are misleading because the architectures provide fundamentally different services. The sectorized mesh with cap=10 monitors 3.2% of sector peers; the hierarchy provides 100% cluster coverage plus fleet-wide summaries. **Required action:** Either (a) design a sectorized mesh variant that provides comparable functionality (e.g., full sector coverage) and compare at equal service levels, or (b) remove quantitative overhead comparisons between the two architectures and present them only as qualitatively different design points.

4. **Coordinator election under RF backup is not adequately validated.** The RF-backup Raft election analysis (Section III-B.2) estimates ~113 s for election over Slotted ALOHA at 1 kbps, but Raft assumes reliable message delivery for correctness (not just liveness). Under Slotted ALOHA with $\gamma \approx 0.36$ and GE losses, the election may not converge or may elect split-brain coordinators. The paper does not analyze Raft correctness under these conditions. **Required action:** Provide a formal argument or simulation evidence that Raft election converges correctly under the assumed RF-backup channel conditions, or propose an alternative election mechanism with proven convergence guarantees under lossy channels.

---

## Minor Issues

1. **Eq. 2 ($W_q$):** The M/D/1 waiting time formula $W_q = \rho / (2\mu_s(1-\rho))$ is correct but should cite the Pollaczek-Khinchine result or note it is the M/D/1 specialization of the P-K formula. The current citation to Kleinrock is sufficient but the equation number should be referenced when used later.

2. **Table I notation:** $\eta$ is defined as "$\eta_0 + \eta_{\text{cmd}}$, beyond baseline" but later text uses $\eta_{\text{total}} = \eta + 20.5\%$. The table should include $\eta_{\text{total}}$ in the notation list for completeness.

3. **Section III-B.2, coordinator processing:** "$\mu_c = 200$ msg/s (5 ms/msg including integrity check)" — the integrity check is not defined. Is this a CRC check, cryptographic verification, or state consistency check? At 5 ms, cryptographic verification seems plausible but should be specified.

4. **Eq. 6 ($\gamma$ derivation):** The guard time calculation assumes 500 km cluster diameter, but this parameter is not in Table III. It should be added or the sensitivity to cluster diameter should be noted.

5. **Table V, "GE + Exc." column:** The dramatic drop from 122,510 to 377 drops at 15 kbps is explained as a "load-reduction effect," but the magnitude (99.7% reduction) deserves more analysis. Is this because exception telemetry reduces offered load by 90% (from $p_{\text{exc}} = 1.0$ to 0.10)?

6. **Section IV-E:** "Fig. 7 confirms all three profiles produce scale-invariant $\eta$ across $N = 10^3$ to $10^5$" — this is a mathematical consequence of $O(N)$ messages with $O(N)$ bandwidth, not an empirical finding. The language should reflect this.

7. **Acknowledgment section:** "Claude 4.6, Gemini 3 Pro, GPT-5.2" — these version numbers do not correspond to any publicly released models as of mid-2025. If these are internal/beta versions, this should be noted; if they are projected future versions, this is inappropriate.

8. **Table III, collision avoidance rate:** $10^{-4}$/node/s yields ~8.6 alerts/node/year. The footnote says these are "screening notifications," but no reference supports this rate. ESA's conjunction statistics [esa_conjunction] should be cited with the specific rate derivation.

9. **Section III-B.3:** The gossip fanout $f = N/\log N$ is described as chosen "for single-cycle convergence," but standard gossip with constant fanout converges in $O(\log N)$ rounds. The choice of $f = N/\log N$ makes the mesh intentionally expensive—this should be more prominently flagged as a worst-case construction.

10. **Eq. 5 ($B_{\text{sector}}^{\text{capped}}$):** Missing the inter-sector summary term (512 B) that appears in the footnote to Table III but not in the equation.

11. **References [5] and [6]:** O'Neill (1976) and Badescu (2006) are cited for "$10^5$–$10^6$ unit" infrastructure concepts, but neither provides engineering-level coordination requirements. These are aspirational references that overstate the near-term relevance of the $10^5$+ regime.

---

## Overall Recommendation

**Major Revision**

The paper addresses a legitimate gap in the literature and provides a well-structured analytical framework for hierarchical coordination sizing. The three-layer feasibility decomposition, the GE sensitivity curves, and the TDMA superframe budget are genuine contributions. However, four issues require substantial revision: (1) the fluid-server/TDMA modeling gap undermines the joint interaction claims; (2) the practical significance is limited by the paper's own finding that constraints are non-binding at normal operating bandwidths; (3) the sectorized mesh comparison is not at equal service levels; and (4) the Raft election under RF-backup conditions lacks convergence analysis. The paper is honest about its limitations but needs to either close the identified gaps or more fundamentally reframe its contributions around what is actually validated. With these revisions, the paper could make a solid contribution to TAES.

---

## Constructive Suggestions

1. **Reframe the contribution around the RF-backup survivability problem.** Rather than presenting general "design equations," position the paper as answering: "What is the minimum coordination capability that survives optical ISL disruption on a 1 kbps RF backup channel?" This reframing aligns the contribution with the regime where the equations are actually binding and avoids the awkwardness of the $\geq$10 kbps triviality result.

2. **Implement TDMA slot scheduling in the DES for at least the single-cluster case.** The slot-level simulator already exists; integrating its logic into the main DES for the joint interaction experiments (Table V) would close the most significant methodological gap. This would also allow direct validation of the half-duplex partitioning constraints (Eqs. 11–12) under combined GE loss and capacity limitation.

3. **Replace the sectorized mesh comparison with a hybrid architecture analysis.** Instead of comparing hierarchical to a functionally different sectorized mesh, analyze a hybrid architecture that uses hierarchical coordination for fleet-wide awareness and local mesh for neighbor monitoring. This would be more operationally relevant and would avoid the apples-to-oranges comparison problem.

4. **Add a concrete mission scenario with end-to-end requirements traceability.** Map the design equations to a specific operational scenario (e.g., Starlink-scale conjunction avoidance during a solar storm that degrades optical ISLs). Show how a system engineer would use Table II, the AoI equation (Eq. 8), and the GE recovery curves (Fig. 5) to size the coordination system. This would dramatically increase the paper's practical impact.

5. **Provide sensitivity analysis on message sizes.** The current results are specific to $S_{\text{eph}} = 256$ B, $S_{\text{cmd}} = 512$ B, $S_{\text{hb}} = 64$ B. Since $\eta_{\text{cmd}}$ dominates the stress case and scales linearly with $S_{\text{cmd}}$, showing how the feasibility boundaries shift with message size (e.g., compressed ephemerides at 128 B, or extended commands at 1024 B) would make the design equations more generally applicable.