---
paper: "02-swarm-coordination-scaling"
version: "aw"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-27"
recommendation: "Major Revision"
---



# Peer Review: "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms"

## Manuscript Version: AW

---

## 1. Significance & Novelty

**Rating: 3 (Adequate)**

The paper addresses a genuine gap: there is no systematic, byte-level traffic accounting framework for comparing coordination architectures at the $10^3$–$10^5$ node scale. The authors correctly identify that swarm robotics literature operates at tens-to-hundreds of agents, constellation management literature treats routing but not autonomous coordination overhead, and no prior work combines these concerns with closed-form sizing equations. The practitioner-oriented "design equation" framing is valuable and distinguishes this from purely theoretical contributions.

However, the novelty is more integrative than fundamental. The individual analytical components—M/D/1 queueing, Gilbert-Elliott channel models, geometric AoI distributions, gossip convergence bounds—are all well-established. The paper's contribution is assembling them into a coherent sizing toolkit, which is useful but incremental. The headline result that architecture-specific overhead is ~5% while commands dominate at >60% is important but also somewhat intuitive: topology-dependent coordination metadata (summaries, heartbeats, election) is naturally small relative to the payload traffic (commands) that any architecture must carry. The paper would benefit from more clearly articulating what *surprising* or *counterintuitive* insight emerges from this analysis.

The operating regime—1 kbps RF backup, <1% of operational time—is narrow and somewhat self-limiting. The authors acknowledge this but the practical impact is constrained: the design equations are most relevant during degraded operations when optical ISLs are unavailable, which is by definition a rare condition. The paper does not adequately address whether the hierarchical architecture provides value during the >99% nominal optical regime, where bandwidth constraints are qualitatively different.

## 2. Methodological Soundness

**Rating: 3 (Adequate)**

The cycle-aggregated DES approach is appropriate for the research questions and the message-layer abstraction is reasonable for a first-order sizing study. The validation against Pollaczek-Khinchine (within 2% at N=100) and gossip bounds (N≤1,000) provides some confidence, though these are relatively easy cases. The 30 MC replications with bootstrap CIs and the open-source code availability are commendable practices.

**Concerns about the simulation fidelity and scope:**

The simulation's ~7s runtime at N=10^5 for a 1-year simulation raises questions about what physical phenomena are being captured. With $T_c = 10$s cycles over one year (~3.15M cycles), processing 10^5 nodes per cycle in 7s implies ~450ns per node-cycle—essentially just accumulating byte counters. This is consistent with the authors' description but means the "simulation" is closer to a vectorized analytical calculator than a discrete-event simulation in the traditional sense. The DES-to-analytical agreement of 0.1% (Table VII) confirms this: the DES is essentially computing the same closed-form expressions with random number generation for loss events. This is not inherently problematic, but the paper should be more forthright that the DES primarily verifies implementation correctness of the analytical model rather than providing independent physical validation.

The abstraction of MAC-layer scheduling is the most significant methodological limitation. The paper derives $\gamma = 0.949$ from a TDMA frame analysis (Eq. 7) but then conservatively uses $\gamma = 0.85$, accounting for FEC, ranging, and control-channel overhead via rough percentages (~7%, ~3%, ~5%). These are asserted without derivation or reference. More critically, the TDMA frame analysis assumes a single-cluster, single-hop scenario. In a four-level hierarchy with 1,000 clusters at N=10^5, the TDMA scheduling problem is substantially more complex: inter-cluster interference, regional coordinator multi-access, and ground-link scheduling are all abstracted away. The claim that "MAC overhead scales by $1/\gamma$" (Section I-C) is an oversimplification that assumes MAC inefficiency is a simple multiplicative factor independent of topology and traffic pattern.

The Gilbert-Elliott model with per-cycle state transitions is a reasonable first-order correlated loss model, but the coherence assumption (GE state constant within $T_c$) is both the model's strength and weakness. The authors correctly note this is conservative for recovery (shorter coherence would help) but do not discuss the opposite case: what if the coherence time is *much longer* than $T_c$ (e.g., structural shadowing lasting minutes)? The per-cycle transition model with $p_{BG} = 0.50$ implies mean bad-state duration of 2 cycles (20s), which may underestimate realistic obstruction durations. The sensitivity sweep (Fig. 5b) partially addresses this but the default parameterization deserves more physical justification.

**Statistical concerns:** The claim of SD < 0.001% for overhead (Section III-D) across 30 replications is consistent with the near-deterministic nature of the byte accounting, but this precision is misleading—it reflects the absence of meaningful stochastic variation in the overhead metric, not the robustness of the result to model uncertainty. The inter-cycle recovery statistics (Fig. 5) are the one area where MC adds genuine value beyond the analytical model.

## 3. Validity & Logic

**Rating: 3 (Adequate)**

The internal logic is generally sound, and the authors are commendably transparent about limitations. The pipeline decoupling result (Section IV-D, Table V) is well-argued: under point-to-point links, GE losses remove messages before coordinator ingress, so loss and capacity are independent. The scope caveat (shared-medium contention breaks this) is appropriately stated.

**Key validity concerns:**

First, the baseline comparison is structurally asymmetric, as the authors acknowledge (Section IV-G). The centralized model captures only compute-queue scalability (M/D/c), while the hierarchical model includes byte-level traffic accounting, link losses, and AoI. The centralized model does not account for uplink scheduling, ground contact windows, or spectrum constraints—which the authors identify as the *actual* binding constraints. This means the paper's central comparison (hierarchical vs. centralized) is comparing apples to oranges: a detailed communication-layer model against a compute-only model. The statement that "a centralized baseline does not diverge computationally until N ≈ 10^6" (abstract, conclusion) is technically correct but potentially misleading, as it implies the centralized approach works fine to 10^6 when the authors themselves note it doesn't.

Second, the sectorized mesh comparison deserves scrutiny. The $k_s = \lceil\sqrt{N}\rceil$ sizing is described as "an order-of-magnitude heuristic" (Section III-B.4), and the capped-fanout variant (heartbeats to min($k_s-1$, 10) neighbors) is the DES implementation. But with cap=10, each node monitors only 3.2% of its sector (Table III). It is unclear whether this provides sufficient situational awareness for conjunction assessment—the stated motivation for the sectorized mesh. The paper compares overhead but not coordination *quality* across topologies (except AoI, which is only analyzed for the hierarchical case).

Third, the static topology assumption is more consequential than the 0.5% overhead bound suggests. The analytical estimate of re-association overhead (Section V-B) considers only byte overhead, but the coordination *disruption*—loss of cluster state, AoI transient, potential missed conjunction alerts during the 1-3 cycle rebuild—could be operationally significant. In a Walker-delta constellation at 550 km with cross-plane drift, re-associations every 45-90 minutes mean ~16-32 events per day per affected node. The cumulative effect on coordination quality is not analyzed.

Fourth, the collision avoidance rate of $10^{-4}$/node/s is described as "screening events, not maneuvers" but the sensitivity analysis ($\pm$1.5 pp impact on $\eta$) suggests this parameter is not consequential for overhead. However, the *latency* and *reliability* requirements for collision avoidance are qualitatively different from routine telemetry, and the equal-priority message model (acknowledged as a limitation in Section V-B) means the paper cannot assess whether the hierarchical architecture meets conjunction response time requirements.

## 4. Clarity & Structure

**Rating: 4 (Good)**

The paper is well-organized with a clear roadmap (Section IV opening paragraph) and consistent notation. The design equations summary (Section V-C) is a valuable practitioner reference. Tables are generally well-constructed, and the traffic accounting (Tables IV, VI, VII) provides the transparency needed to verify claims.

**Strengths:** The explicit separation of baseline telemetry (20.5%) from protocol overhead ($\eta$) and total utilization ($\eta_{\text{total}}$) is clear and consistently maintained. The coordinator link model comparison (Table II) effectively communicates the convergence of different scheduling assumptions. The GE sensitivity sweep (Fig. 5b) is a genuinely useful design artifact.

**Weaknesses:** The paper is dense and could benefit from tightening. At ~12 pages of technical content (estimated from LaTeX source), it pushes the limits of a journal article. Some material is redundant: the overhead value of ~46% is stated at least 15 times across abstract, introduction, results, and conclusion. The notation, while mostly consistent, introduces many symbols without a consolidated notation table (e.g., $\eta$, $\eta_{\text{eff}}$, $\eta_{\text{total}}$, $\eta_{\text{sector}}$, $\eta_0$, $\eta_N$, $\eta_S$, $\eta_E$, $\eta_{\text{delivered}}$, $\eta_{\text{sync}}$).

The abstract is overloaded with specific numerical results that are difficult to parse without context. A more concise abstract focusing on the key insight (architecture-specific overhead is small; commands dominate; pipeline decoupling enables independent sizing) would be more effective.

Figure references suggest 12+ figures, which is high for a journal article. Without seeing the actual figures (only PDF references in the LaTeX), I cannot assess their quality, but the captions are informative. The paper would benefit from consolidating some figures (e.g., combining the sensitivity sweeps).

## 5. Ethical Compliance

**Rating: 4 (Good)**

The AI-assistance disclosure in the Acknowledgment section is appreciated and follows emerging best practices. The statement that AI tools "motivated aspects of the coordinator architecture but [are] not validated here" is appropriately scoped. The open-source code and data availability statement support reproducibility.

The anonymous authorship ("Project Dyson Research Team") with a note about providing names for final publication is unusual but not unprecedented for initial submissions. The self-citation to [45] (dyson_multimodel) is to a non-peer-reviewed online publication, which should be noted.

One concern: the paper references future AI model versions (Claude 4.6, Gemini 3 Pro, GPT-5.2) that do not exist as of my knowledge cutoff. If these are fictional/projected model names, this should be clarified; if the paper is set in a near-future context, this is unconventional for a technical journal submission.

## 6. Scope & Referencing

**Rating: 3 (Adequate)**

The paper is appropriate for IEEE T-AES in scope, addressing autonomous spacecraft coordination with quantitative engineering analysis. The reference list (50 citations) is adequate in breadth, covering constellation operations, swarm robotics, distributed systems, queueing theory, and space standards.

**Gaps in referencing:** The paper does not cite recent work on distributed space systems coordination that is directly relevant: (1) Distributed spacecraft mission planning (e.g., Chien et al.'s earlier work on autonomous scheduling, beyond the 2024 DSA reference); (2) Inter-satellite link scheduling optimization (e.g., Leyva-Mayorga et al., IEEE JSAC 2022, on mega-constellation ISL scheduling); (3) Age of Information in satellite networks (e.g., recent AoI work specific to LEO constellations); (4) The CCSDS Spacecraft Onboard Interface Services (SOIS) standards, which are directly relevant to the message model.

Several references are non-archival (SpaceX FCC filings, Amazon web pages, DARPA program pages, DOD fact sheets). While understandable for operational systems, the paper relies on these for key claims about current constellation scale and operations. The McDowell reference (planet4589.org) is explicitly noted as non-archival, which is good practice.

The Related Work section (Section II) is adequate but somewhat superficial—it lists relevant work without deeply engaging with how prior results inform or contrast with the present analysis. For example, the NASA DSA reference [51] is mentioned in one sentence but the relationship between DSA's onboard decision-making approach and the hierarchical coordination model proposed here is not discussed.

---

## Major Issues

1. **Asymmetric baseline comparison undermines the central claim.** The hierarchical model includes detailed communication-layer analysis (byte accounting, link losses, AoI, GE recovery) while the centralized baseline models only compute-queue scalability (M/D/c). The paper's framing suggests hierarchical coordination is advantageous, but the comparison is not on equal footing. The centralized model should include at minimum: uplink scheduling constraints, ground contact window modeling, and spectrum allocation at scale. Without this, the claim that "the hierarchical advantage is fault tolerance during ground outages" is asserted rather than demonstrated. **Required:** Either equalize the modeling depth across baselines or explicitly restrict all comparative claims to the dimensions that are modeled equivalently.

2. **The DES adds minimal independent validation beyond the analytical model.** The 0.1% DES-to-analytical agreement (Table VII) demonstrates implementation correctness, not physical validity. The paper should clearly distinguish between (a) verification (DES matches closed-form: confirmed) and (b) validation (model matches physical reality: not addressed). The inter-cycle GE recovery statistics (Fig. 5) are the one area where MC provides genuine added value. **Required:** Reframe the DES contribution as verification, not validation; add a discussion of what physical-layer validation would require (e.g., NS-3 simulation, hardware-in-the-loop testing).

3. **The 1 kbps RF-backup operating regime is too narrow to support the paper's broad framing.** The abstract and introduction frame the contribution as addressing coordination of $10^3$–$10^5$ node swarms, but the analysis applies only during RF-backup mode (<1% of operational time). The design equations are parameterized by $C_{\text{node}}$ and scale linearly, but the paper does not demonstrate that the hierarchical architecture's properties (pipeline decoupling, AoI scaling, cluster-size insensitivity) hold at optical ISL rates where the traffic model would be qualitatively different (e.g., full state transfer becomes feasible, eliminating the need for aggregation). **Required:** Either broaden the analysis to include the nominal optical regime or narrow the title and framing to explicitly scope the contribution to degraded-mode operations.

4. **Coordination quality is not compared across topologies.** The paper compares overhead ($\eta$) across all four topologies but only analyzes AoI for the hierarchical case (Table VI). Without AoI, conjunction detection latency, or coordination success metrics for the centralized and sectorized mesh baselines, the overhead comparison is incomplete. A topology with lower overhead but worse coordination quality (or vice versa) would change the design recommendation. **Required:** Extend AoI and coordination success analysis to at least the sectorized mesh baseline.

## Minor Issues

1. **Eq. (2):** The M/D/1 mean waiting time formula $W_q = \rho / [2\mu_s(1-\rho)]$ is correct for M/D/1 but should be explicitly noted as the Pollaczek-Khinchine result with $C_s^2 = 0$ (deterministic service). The current presentation could be confused with the M/M/1 result.

2. **Section III-B.3:** The gossip convergence formula $R_{\text{conv}} = \max(\lceil\log_2 N\rceil, \lceil N/(bf)\rceil)$ appears to be an ad hoc combination of two bounds. The standard epidemic convergence result is $O(\log N)$ rounds for dissemination to all nodes with fanout $f$; the $N/(bf)$ term seems to account for batch transmission constraints. This should be derived or cited.

3. **Table I:** The "Representative System" column (e.g., "Hyperscale data center" for c=1000) is informal and potentially misleading. A hyperscale data center could process far more than $10^7$ nodes at 0.1 msg/s.

4. **Section IV-A, Eq. (8):** $C_{\text{TDMA}} = (k_c - 1) \times S_{\text{eph}} \times 8 / (T_c \times \gamma)$. The $k_c - 1$ (excluding the coordinator itself) is correct but inconsistent with the earlier statement that "each cluster coordinator sends a single 512-byte summary" (Section III-B.2), which implies the coordinator also generates traffic. Clarify whether the coordinator reports to itself or is excluded.

5. **Table V (Joint Interaction):** The "No Loss" and "GE Only" columns are identical, which is the paper's point about pipeline decoupling. However, the "GE + Exc." column shows dramatically fewer drops (e.g., 377 vs. 122,510 at 15 kbps). This is because exception telemetry reduces offered load, not because of any GE interaction. The table conflates two independent effects and should be restructured to separate them.

6. **Section V-B (Static Topology):** The re-association overhead bound of <0.5% assumes one re-association per 90 min per affected node, but "affected node" is not defined. In a Walker-delta constellation, *all* nodes at orbital-plane intersections are affected. The fraction of affected nodes should be estimated.

7. **Acknowledgment:** "Claude 4.6, Gemini 3 Pro, GPT-5.2" — these model versions do not correspond to any publicly released models as of early 2025. If these are projected/fictional, this should be noted; if the paper is written from a future date, this is unconventional.

8. **Notation inconsistency:** $p_{\text{link}}$ (Table VI) appears to be the complement of $p_{\text{loss}}$, but this is not explicitly defined. In Table IV, $p_G$ and $p_B$ are loss probabilities, while $p_{\text{link}}$ in Table X appears to be delivery probability. Unify notation.

9. **Section III-B.2:** "Coordinator rotation: state transfer (10–50 MB) over optical ISL (80–400 ms), excluded from $\eta$." The exclusion is justified but the 10–50 MB range is large (5×). What drives this variation? Is it $k_c$-dependent? This should be parameterized.

10. **Fig. 1 reference:** The architecture diagram (fig-architecture-diagram.pdf) is referenced but not included in the submission. This is critical for understanding the four-level hierarchy.

## Overall Recommendation

**Major Revision**

The paper addresses a real gap in the literature and provides a useful practitioner toolkit for sizing hierarchical coordination in large space swarms. The analytical framework is internally consistent, the open-source code supports reproducibility, and the design equations summary is a valuable reference. However, the contribution is undermined by three structural issues: (1) the asymmetric baseline comparison makes the central architectural comparison inconclusive; (2) the DES is presented as validation when it is primarily verification of the analytical model; and (3) the narrow operating regime (1 kbps RF backup, <1% of time) limits the practical impact relative to the broad framing. These issues are addressable through revision—equalizing the baseline modeling, reframing the DES contribution, and either broadening the analysis or narrowing the scope—but require substantial additional work.

## Constructive Suggestions

1. **Equalize the centralized baseline.** Add uplink scheduling constraints (ground contact windows, per-station capacity, handover) to the centralized model at the same level of detail as the hierarchical communication-layer analysis. This would make the topology comparison credible and likely strengthen the hierarchical case by revealing centralized bottlenecks that the current M/D/c model misses.

2. **Add a "validation gap" section.** Explicitly enumerate what physical-layer phenomena would need to be modeled to validate (not just verify) the design equations: MAC-layer contention, Earth-occlusion link outages, antenna pointing constraints, Doppler effects, and priority queueing. For each, estimate the likely direction and magnitude of impact on the key results. This would transform a limitation into a research roadmap.

3. **Extend AoI analysis to the sectorized mesh.** The sectorized mesh is the most credible alternative to the hierarchical architecture (both are $O(N)$, both are within budget). Comparing AoI, conjunction detection latency, and coordination success across both topologies would provide a genuine architectural trade-off analysis rather than just an overhead comparison.

4. **Consolidate and sharpen the presentation.** The paper repeats key numbers excessively. Consider: (a) a single summary table of all design equations with their domains of validity; (b) reducing the figure count by combining related panels; (c) moving the detailed traffic accounting tables to an appendix; (d) tightening the abstract to ~150 words focusing on the key insight rather than exhaustive numerical results.

5. **Provide physical justification for GE parameters.** The default $p_{BG} = 0.50$ (mean 2-cycle = 20s bad-state duration) should be justified against measured ISL or S-band link statistics. If such data are unavailable, state this explicitly and frame the sensitivity sweep (Fig. 5b) as the primary contribution rather than the default-parameter results.