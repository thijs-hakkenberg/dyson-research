---
paper: "02-swarm-coordination-scaling"
version: "bj"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-27"
recommendation: "Major Revision"
---

# Peer Review: "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms"

**Manuscript Version:** BJ
**Venue:** IEEE Transactions on Aerospace and Electronic Systems

---

## 1. Significance & Novelty

**Rating: 3 (Adequate)**

The paper addresses a genuine gap: there is no published work providing closed-form parametric sizing equations for coordination architectures spanning $10^3$–$10^5$ autonomous space nodes with byte-level traffic accounting. The authors correctly identify that swarm robotics literature operates at 10–100 agents, constellation management at ~10,000, and networking literature treats routing without coordination-layer sizing. The three-layer feasibility decomposition (byte budget, MAC efficiency, TDMA airtime) is a useful conceptual contribution that practitioners could adopt.

However, the novelty is tempered by the nature of the results. The core finding—that architecture-specific overhead is ~5% while command traffic dominates—is essentially a consequence of the assumed message model rather than a deep architectural insight. The closed-form equations (Section V-C) are relatively straightforward: $\eta$ is a linear function of command probability, AoI P99 follows directly from the geometric distribution, and the GE recovery CDF is a standard Markov chain calculation. None of these individually represent significant analytical advances. The contribution is better characterized as a *systems engineering integration* of known results into a coherent sizing framework, which is valuable but should be positioned more modestly.

The paper's relevance to near-term practice is also limited. The authors acknowledge that at ≥10 kbps (the normal operating regime for optical ISLs), all constraints become non-binding (Table I). The 1 kbps RF-backup regime that drives most of the analysis applies to <1% of operational time. While designing for degraded modes is important, the paper could better articulate why the community needs detailed sizing equations for a regime that is both rare and operationally conservative. The $10^5$–$10^6$ scale motivating the work (O'Neill colonies, Badescu macro-engineering) is speculative enough that the practical impact timeline is unclear.

## 2. Methodological Soundness

**Rating: 3 (Adequate)**

The cycle-aggregated DES approach is appropriate for the message-layer analysis claimed, and the authors are commendably transparent about what is and is not modeled. The Monte Carlo configuration (30 replications, bootstrap CIs, per-run-then-aggregate tail statistics) is statistically sound. The analytical cross-checks (overhead agreement <0.1%, AoI P99 matching to within 3 seconds, Markov recovery CDF validated by DES) provide confidence in internal consistency.

However, the methodology has a fundamental circularity problem that limits the strength of conclusions. The DES and the closed-form equations operate at *exactly the same abstraction level*—both count messages and bytes without modeling contention, scheduling, or physical-layer effects. The <0.1% agreement (Table VI) is therefore a verification of implementation correctness, not a validation of the sizing equations against reality. The authors acknowledge this (Section V-A), but the paper's framing sometimes overstates the DES's independent contribution. For instance, the abstract claims the "Monte Carlo tool checks message-layer consistency to <0.1%"—this is accurate but could mislead readers into thinking the equations have been validated against a higher-fidelity model.

The Gilbert-Elliott model is well-motivated but the per-cycle coherence assumption (GE state constant within $T_c = 10$ s) is a strong simplification that the authors themselves note may not hold for all obstruction mechanisms. The physical mapping (Section IV-C) helpfully identifies three regimes, but the admission that the GE model is inappropriate for Earth occultation—likely the dominant outage mechanism in LEO—significantly limits the model's applicability. The claim that the GE model provides "an upper bound on recovery time" is only true for stochastic obstructions; for deterministic occultation, the model is simply inapplicable.

The static topology assumption is reasonable for co-planar formations but problematic for the cross-plane configurations that dominate mega-constellations. The quantitative bound ($f_h = 0.8\%$) is helpful but assumes a single re-association rate; in practice, orbital mechanics create correlated churn events (e.g., at ascending/descending node crossings) that could temporarily affect many clusters simultaneously. This is acknowledged as future work but weakens claims about $10^5$-node applicability.

## 3. Validity & Logic

**Rating: 3 (Adequate)**

The internal logic is generally sound, and the authors are careful to qualify claims. The three-layer feasibility framework is logically coherent: byte budget → MAC efficiency → TDMA airtime scheduling represents a proper nesting of constraints. The distinction between broadcast and unicast command dissemination (Eq. 8, Table V) is an important nuance that is well-handled.

Several logical issues deserve attention. First, the comparison between hierarchical and sectorized mesh architectures is problematic despite the authors' efforts to qualify it. Table IX and the "14× bandwidth efficiency per unit of awareness" metric (Section IV-G) compare architectures with fundamentally different functional scopes—the hierarchy provides fleet command dissemination and full cluster awareness while the capped mesh provides only local monitoring. This is like comparing the fuel efficiency of a sedan and a bicycle; the metric is technically correct but potentially misleading. The capability matrix (Table X) helps, but the 14× figure will likely be cited out of context.

Second, the coordinator failure analysis (Section III-B.2) reveals a significant vulnerability that is somewhat underplayed. The RF-backup handoff requires ~60 seconds (6 cycles), during which ~100 nodes lose coordination. The double-fault scenario (coordinator failure + optical outage) is described as the "design-driving case," yet the paper treats it as a modest concern because AoI impact is "+60 s, modest vs. P99 = 441 s under exception telemetry." This comparison conflates two different AoI regimes: the 441 s P99 occurs under exception telemetry (a bandwidth-saving choice), while the +60 s occurs during a failure (an involuntary outage). A system operating in periodic reporting mode (P99 AoI = 10 s) would experience a 7× degradation during coordinator failure—this deserves more attention.

Third, the claim that "at ≥10 kbps, all constraints are non-binding" (abstract, Table I) is true for the modeled constraints but could create false confidence. At higher bandwidths, currently unmodeled constraints (MAC contention, antenna scheduling, interference) may become binding. The paper should more explicitly state that this conclusion holds only within the message-layer abstraction.

The mission requirements coupling (Section IV-B) is a welcome addition. The comparison of 441 s AoI against 12–72 h TCA windows is well-reasoned, though the caveat about final maneuver decisions requiring AoI < 10 s via optical ISL somewhat undermines the RF-backup sizing exercise.

## 4. Clarity & Structure

**Rating: 4 (Good)**

The paper is well-organized with a clear roadmap (beginning of Section IV) and consistent notation (Table I). The three-layer feasibility framework provides a useful organizing principle. The design equations summary (Section V-C) is a practical contribution that readers can directly apply. The superframe time budget (Table IV) is an exemplary piece of engineering documentation.

The writing quality is generally high, though the paper is extremely dense. At approximately 10,000 words of technical content with 12 tables and 13 figures, it pushes the limits of a journal article. Some material could be moved to supplementary content without loss—for instance, the detailed neighbor-cap sensitivity analysis (Table III) and the duty cycle trade-offs (Table VIII, Fig. 9) are useful but secondary to the main contributions.

The notation is mostly consistent, but there are some confusing choices. The symbol $\eta$ is overloaded: it appears as protocol overhead fraction (Table I), but also as $\eta_E$, $\eta_S$, $\eta_0$, $\eta_{\text{total}}$, $\eta_{\text{eff}}$, $\eta_{\text{sector}}$, and $\eta_{\text{sync}}$—eight variants that require careful tracking. A clearer notational hierarchy would help.

The abstract is accurate but dense to the point of being impenetrable for non-specialists. Phrases like "22-cycle staggering; broadcast commands remain feasible" and "Gilbert-Elliott inter-cycle recovery P95 in 4 cycles with parametric design curves" assume significant domain knowledge. A more accessible abstract would broaden readership.

Figures are referenced appropriately but cannot be evaluated in this review (LaTeX source only). The captions are detailed and self-contained, which is good practice.

## 5. Ethical Compliance

**Rating: 4 (Good)**

The AI-assisted methodology disclosure in the Acknowledgment section is commendable and increasingly important. The statement that "An AI-assisted ideation exercise (Claude 4.6, Gemini 3 Pro, GPT-5.2) motivated aspects of the coordinator architecture but is not validated here" is appropriately scoped. The reference to a separate methodology paper [44] provides traceability.

The anonymous authorship ("Project Dyson Research Team") with a note that "Individual author names and affiliations will be provided for final publication per IEEE policy" is unusual but acceptable for review. IEEE policy does require named authors for publication.

The open-source data availability statement with a specific repository tag (`paper-02-v-bj`) and computational environment specification supports reproducibility. This is exemplary practice.

One concern: the paper references future model versions (Claude 4.6, GPT-5.2) that do not exist as of mid-2025, suggesting either the paper is set in a near-future context or these are placeholder names. This should be clarified to avoid confusion about the provenance of AI-assisted contributions.

## 6. Scope & Referencing

**Rating: 3 (Adequate)**

The paper is appropriate for IEEE TAES in scope, addressing autonomous spacecraft coordination at scale. The reference list (52 entries) covers the major relevant areas: constellation operations, distributed systems theory, swarm robotics, queueing theory, and space standards.

However, several important gaps exist in the referencing. The paper does not cite recent work on distributed space systems coordination that has appeared since 2020, particularly in the context of LEO mega-constellation autonomy. Works on autonomous collision avoidance decision-making (e.g., Sanchez-Ortiz et al., Merz et al.) are relevant given the conjunction screening use case. The AoI literature is cited but the specific application of AoI to satellite networks (e.g., work by Uysal, Modiano's group on scheduling for AoI in satellite systems) deserves mention.

The CCSDS standards citations are appropriate and lend credibility to the message sizing assumptions. However, the paper would benefit from citing actual ISL link budgets or measured channel statistics from operational systems—even if only to note their absence from the public literature.

Several references are non-archival (Amazon Kuiper overview, DARPA program pages, DoD fact sheets, NRL magazine article). While understandable given the operational nature of the field, this weakens the scholarly foundation. The authors should note which references are non-archival, as they partially do for [1].

The O'Neill [5] and Badescu [6] references motivating the $10^5$–$10^6$ scale are from 1976 and 2006 respectively. More recent references on large-scale space infrastructure concepts would strengthen the motivation.

---

## Major Issues

1. **Validation gap undermines the central contribution.** The paper's title promises "design equations," but these equations are validated only against a DES operating at the identical abstraction level. The <0.1% agreement demonstrates implementation correctness, not physical validity. The paper needs either: (a) a clear, prominent statement that all results are message-layer predictions pending physical-layer validation, with explicit uncertainty bounds on how MAC contention, antenna scheduling, and link-layer effects might modify the results; or (b) at minimum a single-cluster NS-3 validation for the TDMA superframe (which the authors identify as the priority next step but have not performed). Without (a) or (b), the "design equations" framing overpromises.

2. **The 1 kbps design point is simultaneously the paper's focus and its least relevant regime.** The authors acknowledge that at ≥10 kbps all constraints are non-binding, and that the 1 kbps RF backup applies <1% of the time. Yet the majority of the analysis (coordinator ingress sizing, TDMA frame design, unicast staggering, half-duplex partitioning) is specific to this regime. The paper should either: (a) reframe as explicitly studying the degraded-mode design problem (which is legitimate and important), or (b) provide comparable analytical depth for the 10–100 kbps regime where most operations occur. Currently, the 10+ kbps regime is dismissed in a single row of Table I.

3. **The sectorized mesh comparison is structurally unfair despite extensive caveats.** The capped sectorized mesh (cap=10, 3.2% sector coverage) is not a coordination architecture—it is a local monitoring scheme. Comparing its overhead to the hierarchy's (which provides full cluster awareness, command dissemination, and aggregation) is comparing different services. The "14× bandwidth efficiency per unit of awareness" metric normalizes by peers monitored but not by functional capability. The paper should either: (a) implement a sectorized mesh with comparable functional scope (which would require higher overhead, likely exceeding the budget), or (b) remove the direct overhead comparison and present the mesh only as a "local awareness baseline" without efficiency ratios.

4. **Correlated failure modes are absent.** The paper models only i.i.d. exponential node failures (2%/yr). For mega-constellations, the dominant failure concerns are correlated: solar particle events affecting entire orbital planes, batch manufacturing defects, software update failures propagating through clusters, and ground segment outages. The coordinator failure transient analysis (Section III-B.2) considers single and double faults but not correlated failures affecting multiple coordinators simultaneously. At $N = 10^5$ with $k_c = 100$, there are 1,000 coordinators; a correlated event affecting even 1% of them (10 coordinators, 1,000 nodes) would stress the system in ways not captured by the current model.

---

## Minor Issues

1. **Eq. (2):** The M/D/1 waiting time formula $W_q = \rho / (2\mu_s(1-\rho))$ is the standard result but should note it applies to the waiting time in queue, not total sojourn time ($W = W_q + 1/\mu_s$).

2. **Table II (Simulation Parameters):** The collision avoidance rate footnote says "Screening events, not maneuver-triggering" but the message is labeled "Collision avoidance msg" (128 B) and described as "Priority alert." Clarify whether these are screening notifications or actionable alerts—the distinction matters for priority queueing (which is listed as a limitation).

3. **Section III-B.2:** "Raft election over optical ISL (RequestVote: 100 B × quorum of ~5 at Gbps rates ≪ 1 ms)" — a quorum of 5 implies a Raft cluster of 9–10 nodes, but the text elsewhere implies the entire cluster ($k_c = 100$) participates. Clarify the Raft group size and how it relates to $k_c$.

4. **Eq. (6):** $B_{\text{sector}}^{\text{capped}} = 256 + \min(k_s - 1, 10) \times 32$ bytes — this omits the inter-sector summary (512 B) mentioned in the text ("512 B inter-sector summaries at boundaries"). The Table III footnote includes commands but not inter-sector summaries. Reconcile.

5. **Table V (Schedulability):** The "Stress (bcast)" row shows single-cycle feasibility (✓) but the byte-budget $\eta_{\text{total}}/\gamma = 78\%$. Clarify that "1-Cycle?" refers to TDMA airtime feasibility, not byte-budget feasibility—both are needed.

6. **Section IV-B:** "AoI P99 exceeds 440 s" at $p_{\text{exc}} = 0.10$ — but the table shows P99 = 441 s and the analytical formula gives 440 s. The 1 s discrepancy is within CI but the text should be consistent.

7. **Table VII (Joint Interaction):** The "GE + Exc." column shows dramatically fewer drops than "No Loss" at 15 kbps (377 vs. 122,510). This is because exception telemetry reduces offered load. This is not a "cross-domain benefit" of GE + exception interaction—it is simply the effect of reduced load. The framing is misleading.

8. **Section III-D:** "Processing delay: Deterministic 5 ms" — this is unusually high for modern embedded processors handling 256 B messages. A brief justification (e.g., including cryptographic verification) would help.

9. **Acknowledgment:** "Claude 4.6, Gemini 3 Pro, GPT-5.2" — these model versions do not exist as of mid-2025. Clarify whether these are future projections or errors.

10. **Throughout:** The paper uses both "kbps" and "bps" without always being explicit about whether these are message-layer or PHY-layer rates. A consistent convention (e.g., always message-layer unless marked with subscript "PHY") would reduce ambiguity.

11. **Fig. 7 caption:** "Dashed: exception telemetry ($p_{\text{exc}} = 0.30$)" — but the text discusses $p_{\text{exc}} = 0.10$ as the primary exception case. Clarify why 0.30 is shown in the figure.

---

## Overall Recommendation

**Major Revision**

The paper addresses a legitimate gap in the literature and provides a well-structured systems engineering framework for sizing hierarchical coordination in large space swarms. The three-layer feasibility decomposition, the TDMA superframe budget, and the GE recovery design curves are useful contributions. However, the central claim of providing "design equations" is undermined by the absence of any validation beyond the message-layer abstraction at which the equations were derived. The DES confirms implementation correctness but not physical validity. The focus on the 1 kbps regime (which applies <1% of operational time) needs better justification or rebalancing. The sectorized mesh comparison, despite extensive caveats, remains structurally unfair due to incomparable functional scope. A major revision should address the validation gap (at minimum through explicit uncertainty quantification for unmodeled effects), reframe the 1 kbps focus, and either equalize the mesh comparison or remove direct efficiency ratios. The paper has the potential to be a solid contribution to the spacecraft autonomy literature if these issues are addressed.

---

## Constructive Suggestions

1. **Perform or scope a single-cluster NS-3 validation.** Even a simplified TDMA simulation with 100 nodes, realistic guard times, and packet-level accounting would dramatically strengthen the paper. If infeasible for this revision, provide explicit *uncertainty bands* on the design equations by analyzing how MAC contention ($\gamma$ variation), timing jitter, and packet errors would modify each equation. The superframe budget (Table IV) already provides the specification—use it to bound the gap.

2. **Add a "10 kbps nominal operations" analysis section.** Mirror the depth of the 1 kbps analysis for the regime where most operations occur. Show which design equations simplify, which new constraints emerge (e.g., interference management, multi-hop routing), and what the operational design envelope looks like. This would make the paper relevant to near-term constellation operators, not just degraded-mode designers.

3. **Replace the hierarchical-vs-mesh efficiency ratio with a Pareto analysis.** Plot overhead vs. functional scope (e.g., number of peers monitored, command dissemination capability, fault tolerance level) for both architectures across their parameter ranges. This would provide a fair comparison that acknowledges the different services each architecture provides, and would be more useful to designers choosing between approaches.

4. **Add a correlated failure scenario.** Model a single correlated event (e.g., 5% of coordinators failing simultaneously, representing a solar particle event or software fault) and characterize the system's recovery trajectory. This would address the most significant gap in the failure analysis and is feasible within the existing DES framework.

5. **Tighten the abstract and reframe the contribution.** The abstract should clearly state: (a) these are message-layer equations pending physical-layer validation; (b) the 1 kbps regime is the design-driving degraded mode, not the normal operating point; (c) the primary value is the sizing framework and design curves, not the specific numerical results (which depend on assumed message sizes and rates). This honest framing would actually increase the paper's impact by setting appropriate expectations.