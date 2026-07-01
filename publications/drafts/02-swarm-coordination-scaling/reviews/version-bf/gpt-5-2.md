---
paper: "02-swarm-coordination-scaling"
version: "bf"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-02-27"
recommendation: "Unknown"
---

## 1. Significance & Novelty — **Rating: 4/5 (Good)**

The manuscript targets a real and timely problem: coordination and communications sizing for autonomous swarms in the \(10^3\)–\(10^5\) node regime. The emphasis on *closed-form sizing relationships* (rather than only simulation) is valuable for practitioners, and the paper’s attempt to “assemble” queueing/AoI/Markov results into a coherent toolkit is aligned with T-AES readership. The explicit byte-level accounting under a fixed per-node budget, together with coordinator-ingress sizing and recovery tail characterization, is a useful integration that is not commonly presented end-to-end in the mega-constellation literature.

Novelty is primarily *synthetic* rather than *fundamental*: most constituent tools (AoI geometric tails, GE recovery, TDMA efficiency, \(M/D/1\) baselines) are standard, but their combination into a parametric sizing guide for hierarchical coordination at these scales is still a meaningful contribution. The strongest “new” element is the systematic separation of (i) topology-dependent overhead (~5%) from (ii) workload-dependent command traffic that dominates stress cases, and the careful discussion that stress-case \(\eta\) is an information-demand upper bound rather than a schedulability guarantee (Section IV-A, Eq. (28)).

That said, several claims in the abstract/contributions read stronger than what is actually validated (e.g., “operationally representative” workload; “coordinator bottleneck vanishes at \(\ge 10\) kbps”; “AoI and recovery equations are bandwidth-independent”): these are plausible within the *message-layer* model, but would benefit from stronger justification and clearer boundaries on applicability (e.g., half-duplex constraints, MAC contention, contact outages). Overall significance is good, but the paper would be stronger if it tightened the mapping from assumptions to operational regimes and clarified which results remain robust under more realistic link/network constraints.

---

## 2. Methodological Soundness — **Rating: 3/5 (Adequate)**

The DES framework is clearly described as cycle-aggregated and message-layer (Section III-A), and the authors are commendably explicit that DES agreement with closed forms validates *arithmetic consistency* rather than PHY fidelity. The parameter tables are detailed (Table II), and the paper provides many analytic cross-checks (e.g., AoI P99 Eq. (33), coordinator ingress Eq. (24), GE recovery derivation in Section IV-C). The open-source release and tag improves reproducibility substantially.

However, several modeling choices materially affect the central sizing conclusions, and the manuscript sometimes treats them as “conservative” without fully demonstrating conservatism in the relevant direction. Examples: (i) GE coherence fixed for the entire cycle (Section IV-C) makes intra-cycle retransmission ineffective “by construction,” which is acknowledged, but then used to motivate inter-cycle recovery; this is fine, but it means conclusions about retransmission utility are conditional on a strong coherence-time assumption. (ii) The coordinator half-duplex TDMA timing budget is tight even without retransmissions (Section IV-A “Half-duplex TX/RX partitioning”); small changes in guard time, PHY rate, or additional control overhead could break feasibility. (iii) The “token bucket” model (Model B) is used as a proxy for scheduling quality, but its mapping to a realizable medium access mechanism in a distributed RF backup scenario is not fully articulated.

Statistically, the Monte Carlo replication count (30) is reasonable for mean overhead and for the AoI P99 methodology (Table VII footnote is good practice). But tail claims like “maximum observed streaks are 10–13 cycles” (Section IV-C) are not stable with only 30 replications unless the number of loss events is extremely large and independent; the paper should clarify the effective sample size for streaks and provide uncertainty bounds for P95/P99 recovery metrics (not only point estimates). Also, several results are presented as scale-invariant across \(N\), but the DES is cycle-aggregated with static clusters; it would help to show at least one sensitivity where cluster churn or contact outages are introduced—even in simplified form—to test whether the claimed invariances persist.

---

## 3. Validity & Logic — **Rating: 3/5 (Adequate)**

Many conclusions are logically supported *within the stated abstraction*: overhead decomposition (Fig. 10), scale invariance of \(\eta\) (Table X, Fig. 12), and AoI geometric tail prediction (Eq. (33) vs Table VII) are consistent and persuasive. The paper is careful to condition hierarchical-vs-mesh overhead comparisons on functional scope (Section III-B4; Table XIV), which is an important and often-missed nuance.

The main concern is that some “design equation” outputs are presented with an implicit air of operational implementability, while later text clarifies that they are information-budget bounds and that schedulability can fail (e.g., stress-case unicast requires 22 cycles, Eq. (28)). This is a good clarification, but it creates tension with earlier messaging (abstract: “commands dominate stress-case … topology-invariant”; “broadcast commands are single-cycle feasible”; “coordinator ingress requires 21–25 kbps under TDMA”). In particular, the stress-case \(\eta \approx 46\%\) is repeatedly used as a headline number, but for the RF-backup half-duplex coordinator it is not deliverable in-cycle under unicast and is only deliverable under broadcast semantics; the manuscript should more consistently separate *byte-budget* from *frame-time feasibility* throughout, not only in Section IV-A.

Similarly, the statement “At \(\ge 10\) kbps the coordinator bottleneck vanishes” (Abstract/Table I) is not fully established: the bottleneck depends on \(k_c\), \(T_c\), half-duplex partitioning, and whether ingress/egress share the same RF chain. Increasing per-node budget does not necessarily change coordinator ingress instantaneous PHY needs unless the architecture changes (e.g., higher PHY, different duplexing, different scheduling). If the intended meaning is “for typical PHYs that accompany 10 kbps average budgets, instantaneous coordinator PHY can be provisioned so drops vanish,” that needs to be stated explicitly and supported by a short feasibility calculation.

Limitations are acknowledged (Section V), but a few are central enough that they should be elevated earlier: Earth occultation (tens of minutes) directly challenges the “<1% operational time” RF-backup framing and strongly affects AoI/recovery tails; shared-medium MAC contention could invalidate the independence claim in Section IV-D; and static clustering could meaningfully affect coordinator duty cycle and handoff costs in cross-plane constellations. These do not invalidate the paper, but they do require tighter scoping of conclusions.

---

## 4. Clarity & Structure — **Rating: 4/5 (Good)**

The manuscript is generally well organized, with a clear roadmap (start of Section IV) and consistent terminology (\(\eta\), \(\eta_{\text{total}}\), \(C_{\text{node}}\), \(C_{\text{coord}}\), \(\gamma\)). Tables are helpful and unusually explicit about what is and is not included in overhead accounting (e.g., Table VI; Section III-F). The abstract is dense but informative and mostly consistent with the body.

That said, the paper occasionally overloads the reader with many “headline numbers” that depend on subtle distinctions (average vs instantaneous rate; information bytes vs PHY transmissions; stress-case vs event-driven; broadcast vs unicast). Section IV-A does address these carefully, but the same care is not consistently reflected in the abstract, contributions list, and early framing. Consider adding a short “Interpretation guide” box near Section III-F that explicitly defines: (i) information budget vs schedulability; (ii) per-node average budget vs coordinator instantaneous PHY; (iii) which results assume dedicated links vs shared medium.

A few internal inconsistencies and presentation issues reduce clarity. Example: Table VI “Coordinator ingress: TDMA … 24 kbps, \(\gamma=0.85\), Raw link 28 kbps” is potentially confusing because earlier Eq. (25) gives \(\gamma \approx 0.949\) and then “conservatively retaining 0.85”; the table could explicitly state whether 24 kbps is *effective* or *raw* and which \(\gamma\) is applied. Also, some figures are referenced but not fully described in-text (e.g., Fig. 9 TDMA comparison—what are axes/assumptions precisely). Finally, the manuscript would benefit from a concise summary table of “assumptions by result” (e.g., AoI assumes geometric exception process; GE assumes per-cycle coherence; coordinator sizing assumes TDMA slots and dedicated ingress).

---

## 5. Ethical Compliance — **Rating: 4/5 (Good)**

The manuscript includes an explicit disclosure of AI-assisted ideation in the Acknowledgment and cites a related internal document (\cite{dyson_multimodel}). This is aligned with emerging transparency expectations. No human-subjects or sensitive data issues are apparent. The open-source release also supports research integrity.

Two items merit improvement. First, the “Project Dyson Research Team” authorship placeholder is understandable for review, but for IEEE compliance the final version must provide full author list, affiliations, and contributions; the current placeholder should be accompanied by a statement that the submission is anonymized for review if that is the intent (IEEE T-AES is typically single-blind, not double-blind). Second, the AI disclosure would be stronger if it specified *where* AI tools were used (ideation only vs writing vs coding) and confirmed that all results were independently verified by the authors (especially given the “AI-assisted ideation exercise” wording).

---

## 6. Scope & Referencing — **Rating: 4/5 (Good)**

The topic is well within IEEE T-AES scope: autonomous spacecraft operations, constellation-scale coordination, communication architecture sizing, and robustness. The manuscript connects to constellation routing/ISL literature (Handley, del Portillo, Bhattacherjee), distributed systems (Lynch, Raft), and AoI theory (Yates survey). Referencing is generally adequate and relatively up to date through 2024, with some non-archival sources clearly labeled.

Opportunities remain to strengthen grounding in space communications/operations practice. For example, the RF-backup regime assumptions (1 kbps average per node, <1% time) and the claim that optical ISL availability is >99% are central but not well referenced; adding citations to Starlink/Kuiper-style optical ISL availability studies (if available) or CCSDS/mission reports would help. Likewise, the “Earth occultation” discussion is important but appears late; a reference for typical ISL blockage statistics or geometry would strengthen the mapping from GE parameters to physical regimes. Finally, the “sectorized mesh” model uses a heuristic \(\sqrt{N}\) argument; it would benefit from citations to conjunction screening/locality literature or at least a short derivation in an appendix.

---

## Major Issues

1. **Byte-budget vs schedulability is not consistently enforced across results and headline claims.**  
   Section IV-A correctly distinguishes information content (\(\eta\)) from TDMA frame-time feasibility and shows unicast commands require 22 cycles (Eq. (28)). However, the abstract, Table I, and multiple “stress-case” discussions still read as if \(\eta_{\text{stress}}\) is an achievable operational mode in the RF-backup regime. The paper should systematically label stress-case as “information upper bound” and explicitly state the required assumptions (broadcast vs unicast; multi-cycle staggering; higher egress PHY; full-duplex; separate chains).

2. **Coordinator RF half-duplex timing budget is extremely tight and under-modeled.**  
   With \(k_c=100\), ingress consumes ~9.18 s of a 10 s cycle (Section IV-A), leaving ~0.8 s for all egress + control. This leaves little margin for additional control traffic, ranging, re-sync, retransmissions, or guard-time inflation. The manuscript should provide a more complete TDMA superframe budget (including sync, possible ACK/NACK, contention slots, re-sync overhead) and quantify margin under nominal and degraded conditions. Without this, the “24 kbps TDMA feasible” claim is fragile.

3. **GE model coherence assumption drives retransmission conclusions “by construction.”**  
   The paper acknowledges this (Section IV-C), but then uses the resulting poor intra-cycle recovery to motivate design choices. The manuscript should either (i) add a second GE variant with sub-cycle transitions (fast-mixing) to show the crossover where intra-cycle retransmissions become useful, or (ii) clearly scope the conclusion to “slow-mixing obstructions” and avoid general statements about retransmission ineffectiveness.

4. **Centralized baseline is not commensurate with the communication-layer analysis and may mislead.**  
   The paper notes the asymmetry (Section IV-G), but the centralized plots/tables (e.g., Fig. 16, Table XIII) still visually compare compute-queue divergence to communication overhead. Consider moving centralized compute-queue results to an appendix or reframing them as a *separate* baseline dimension (compute vs comm) to avoid readers inferring an apples-to-apples architecture comparison.

5. **Static clustering and handoff costs are central to hierarchical feasibility but are only lightly stress-tested.**  
   The paper asserts re-association overhead <0.5% and modest AoI transient (Section V-B), but this is not demonstrated in the DES results. Given that cross-plane mega-constellations have regular geometry-driven neighbor changes, at least one experiment with periodic churn (even simplified) should be included to validate that overhead and AoI tails remain within claimed bounds.

---

## Minor Issues

1. **Equation/notation consistency:**  
   - Table I uses \(\eta_{\text{stress}}\) scaling with bandwidth (46%, 4.6%, 0.46%). This is true only if command bytes are held constant while \(C_{\text{node}}\) scales; consider adding “holding message model fixed” explicitly.  
   - Eq. (24) uses \((k_c-1)\) in TDMA capacity; earlier coordinator demand is based on \(k_c\) members. Clarify whether coordinator itself sends a report or not; the manuscript alternates between \(k_c\) and \(k_c-1\) in several places.

2. **TDMA \(\gamma\) presentation:**  
   Eq. (25) derives \(\gamma=0.949\) but the rest of the paper largely uses 0.85. Consider standardizing: define \(\gamma_{\text{slot}}\) (pure framing) and \(\gamma_{\text{system}}\) (including FEC/control/ranging), and use the latter consistently in all capacity tables/figures.

3. **Figure file/reference issue:**  
   Fig. 14 includes `\includegraphics{fig-cross-cycle-recovery}` without extension while others use `.pdf`. Ensure compilation consistency.

4. **AoI sampling methodology clarity:**  
   Table VII footnote is good, but readers may still confuse AoI sampling every 100 s with AoI evolution at 10 s cycles. A one-sentence clarification in Section IV-B would help: AoI is updated per cycle but sampled every 100 s for storage efficiency (if that is the reason).

5. **Capability matrix (Table XIV):**  
   “Fits 1 kbps budget” shows centralized as “--- uplink-limited.” This is ambiguous: centralized still consumes node uplink bandwidth. Consider rewording to “Not modeled / depends on ground link” or quantify the implied uplink per node for fairness.

6. **Some numeric claims need citations or qualification:**  
   - “optical ISL availability >99%” (Abstract/Contributions) lacks a strong archival reference.  
   - “RF-backup <1% of operational time” similarly needs justification or should be presented as an assumed design target.

---

## Overall Recommendation — **Major Revision**

The manuscript is promising and potentially publishable: it provides a coherent set of sizing equations, careful byte-level accounting, and an open-source consistency-checking DES. However, several central claims (especially around coordinator feasibility, stress-case interpretation, and retransmission/recovery behavior) depend on tight timing and strong channel/MAC assumptions that are not yet sufficiently stress-tested or consistently communicated. Addressing the major issues above—particularly a more complete TDMA timing budget, clearer separation of information budget vs schedulability, and at least one churn/fast-mixing sensitivity—would substantially strengthen validity and reduce the risk of readers overgeneralizing the results.

---

## Constructive Suggestions

1. **Add a “Schedulability vs Information Budget” summary table and enforce it throughout.**  
   For each workload (Nominal/Event-driven/Stress), state: broadcast vs unicast; single-cycle feasible at 24 kbps half-duplex?; if not, required cycles or required PHY. Then ensure the abstract and conclusions use the same language.

2. **Provide a complete TDMA superframe time budget with margin.**  
   Include ingress slots, guard, sync beacon, command broadcast, heartbeat, optional ACK/NACK (if any), and contingency re-sync. Quantify remaining slack under nominal and degraded \(\gamma\). This will make the 21–25 kbps coordinator sizing claim much more defensible.

3. **Extend the GE study with a sub-cycle transition (fast-mixing) variant.**  
   Even a simple modification (GE transitions every \(\tau_c\) seconds with \(m=T_c/\tau_c\)) would allow you to demonstrate the crossover where intra-cycle retries become effective, supporting the “regime condition” discussion already present in Section IV-C.

4. **Include one DES experiment with cluster churn/handoffs.**  
   Implement periodic reassociation for a fraction of nodes (e.g., 10% of nodes change cluster every 60–90 minutes) and report impact on \(\eta\), AoI P99, and coordinator drops. This directly addresses a key limitation and increases operational credibility.

5. **Reframe the centralized baseline to avoid apples-to-oranges comparisons.**  
   Either (i) add a simple comm-layer model for centralized uplink scheduling/bandwidth, or (ii) clearly separate compute scalability plots from comm overhead plots (e.g., two panels) and reduce the prominence of centralized in the main comparison table/figure.