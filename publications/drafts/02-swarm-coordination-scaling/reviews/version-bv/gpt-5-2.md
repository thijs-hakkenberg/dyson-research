---
paper: "02-swarm-coordination-scaling"
version: "bv"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-02-27"
recommendation: "Unknown"
---

## 1. Significance & Novelty — **Rating: 4/5 (Good)**

The manuscript tackles a genuinely important problem: how to *size* coordination communications for very large autonomous spacecraft swarms (10³–10⁵ nodes) under a strict per-node bandwidth budget. The paper’s emphasis on **closed-form sizing equations** (byte budget, MAC efficiency via \(\gamma\), and TDMA airtime feasibility) is a valuable contribution for early-phase architecture trades, where practitioners need order-of-magnitude answers before committing to detailed PHY/MAC design. The explicit separation into “feasibility layers” is a useful conceptual framing and—if tightened—could become a reusable template for constellation coordination sizing.

The strongest novelty is the **byte-level accounting** combined with (i) hierarchical aggregation, (ii) explicit coordinator ingress sizing, and (iii) the observation that under the chosen semantics, **stress-case command traffic dominates and is topology-invariant**. The paper also contributes practical “design curves” for correlated loss recovery using a GE model (Section IV-C), which is relevant to intermittent ISLs and obstruction-driven outages.

That said, the novelty claim should be moderated in two ways. First, parts of the analysis resemble well-known WSN clustering and aggregation sizing (e.g., LEACH-like accounting), though applied to different constraints; the paper should more explicitly articulate *what is fundamentally different in space* (half-duplex superframe, long coherence obstructions, coordinator rotation constraints, etc.) and why existing approaches do not already yield equivalent sizing relationships. Second, the “topology-invariant command traffic” conclusion is only true under a specific decision model (central command generation, fixed message sizes, and per-cycle command semantics). This is acknowledged, but it is central enough that it should be elevated earlier and framed as a conditional result rather than a general property of hierarchical coordination.

---

## 2. Methodological Soundness — **Rating: 3/5 (Adequate)**

The methods are generally appropriate for the stated goal: derive closed-form sizing equations and cross-check them with a fast cycle-aggregated DES plus a slot-level TDMA simulator for a single cluster. The separation of concerns—message-layer DES for scaling and tail metrics; slot-level TDMA sim for superframe feasibility—is sensible and improves reproducibility. The paper also does a good job stating many parameters explicitly (Table III / Table `sim_params`) and providing code availability.

However, there are several methodological mismatches between what is *claimed* and what is *actually modeled* that weaken the soundness:

* **DES does not enforce TDMA airtime constraints** (explicitly noted later in Section IV-D), yet many results are presented as if they describe operational feasibility in the 1 kbps RF-backup regime. The manuscript does provide analytical checks (Eqs. 25–26, Table `superframe`) and a slot-level sim, but only for one cluster and under a narrow set of assumptions. As written, the boundary between “byte-budget feasible” and “airtime feasible” is easy to miss, and some tables (e.g., Table `link_availability`) mix regimes and retransmission assumptions in a way that can confuse readers.

* The **coordinator ingress** is modeled as a *fluid server with drop-tail* (Section III-A), which can underestimate deadline misses and overestimate service regularity relative to any slotted/half-duplex implementation. This is acceptable for byte accounting, but then the paper needs to be more disciplined about which conclusions rely on fluid assumptions versus slotted ones.

* The statistical approach is mostly fine (30 replications, bootstrap CIs), but some reported tail metrics (AoI P99) are essentially deterministic under the model (geometric inter-arrival), and the paper could simplify by emphasizing analytic derivations and using simulation primarily for verification. Conversely, for availability and failure recovery (Section III-B coordinator failure transient; Section IV-H duty cycle), the paper uses “illustrative” Markov reasoning without enough detail to be technically auditable.

Overall, the methodology is promising and largely reproducible, but it needs clearer “model-to-claim” alignment and more careful handling of the boundary between message-layer and slot-/packet-layer realities.

---

## 3. Validity & Logic — **Rating: 3/5 (Adequate)**

Many conclusions are logically supported **within the declared model**. Examples: the AoI P99 under exception telemetry follows directly from the geometric inter-report interval (Eq. 30), and the DES agreement is good. The coordinator ingress requirement (roughly \((k_c-1)\cdot256\text{B}/T_c\)) is also straightforward and consistent with Table `superframe`. The GE argument that intra-cycle ARQ is ineffective under per-cycle coherence is correct, and the Markov recovery derivation is plausible and validated against the DES (Fig. `cross_cycle_recovery`).

The main validity concern is that several headline statements in the abstract and conclusions blur the distinction between (a) **information/byte budget feasibility** and (b) **schedulability under half-duplex TDMA with losses, guard times, and retransmissions**. For instance, the abstract claims “Coordinator ingress requires 24 kbps under half-duplex TDMA with 623 ms per-cycle margin,” but later the paper recommends 30 kbps to avoid ARQ infeasibility and tight margins (Section IV-A). The 24 kbps point is extremely tight (Table `superframe`), and the paper itself shows that even modest degradation in \(\gamma\) or retransmission airtime breaks the schedule. The conclusion should therefore be phrased as: 24 kbps is the *minimum no-loss schedulable point* under optimistic assumptions; a practical design point is ~30 kbps (or more, depending on ranging/FEC/control).

A second logic issue is the claim that at \(\ge 10\) kbps “all message-layer constraints are non-binding.” This is true only if coordinator PHY scales proportionally and if scheduling/pointing/visibility constraints do not introduce new bottlenecks—which the paper acknowledges as “unmodeled constraints may dominate.” The statement should be softened: message-layer byte constraints relax, but system-level feasibility may still be dominated by multi-link scheduling, antenna time-sharing, and crosslink topology dynamics.

Finally, the centralized baseline is intentionally compute-limited and not communication-modeled (Section III-B, Table `topology_comparison`). That is acceptable as a bound, but the paper should avoid implying that centralized coordination “scales” to 10⁶ in any operational sense; it scales in *compute queueing only*.

---

## 4. Clarity & Structure — **Rating: 4/5 (Good)**

The manuscript is generally well organized and unusually explicit about parameters, definitions, and what is and is not modeled. The “three feasibility layers” framing is clear and helpful. Tables are informative (notably Table `superframe`, Table `schedulability`, Table `inflection`) and the paper does a good job cross-checking analytic and simulation results. The abstract is dense but mostly accurate.

That said, the paper is at risk of overwhelming readers with many numbers and regimes. Several places would benefit from clearer signposting:

* The distinction between **\(\eta\)** (beyond baseline) and **\(\eta_{\text{total}}\)** (including baseline) is defined, but the narrative sometimes jumps between them. Consider adding a small boxed definition early (end of Section I-C or start of Section III-F) and consistently labeling plots/tables with “beyond baseline” vs “total utilization.”

* The introduction and contributions emphasize “closed-form sizing equations,” but the paper often presents results first and equations later. A short “Design Equations Overview” figure/table early (perhaps after Table I notation) that lists the key equations and what they size (ingress kbps, \(\eta\), AoI P99, unicast staggering) would improve accessibility.

* Some terms are potentially confusing to non-specialists: “1 kbps per node is a budget, not PHY rate” is important and well stated (Section III-F), but it should be reiterated when discussing 24 kbps TDMA PHY, because otherwise it appears inconsistent.

Overall readability is good for an IEEE TAES audience, but tightening the narrative around the model boundaries would prevent misinterpretation.

---

## 5. Ethical Compliance — **Rating: 4/5 (Good)**

The manuscript contains an explicit disclosure in the Acknowledgment that AI-assisted ideation influenced aspects of the architecture, with a citation. This is better than typical current practice and aligns with emerging transparency expectations. The paper also provides open-source code and data, supporting reproducibility.

Two improvements are recommended for stronger compliance and clarity:

1. The disclosure should specify **what** AI tools contributed (e.g., “brainstorming architecture options,” “drafting text,” “code assistance,” etc.) and confirm that all results were produced/verified by the authors’ simulations/analysis. As written, “motivated aspects” is somewhat vague.

2. IEEE TAES sometimes expects clearer conflict-of-interest and authorship accountability statements. Since author names/affiliations are deferred, ensure the final version includes standard disclosures (funding, conflicts, export control/ITAR considerations if applicable). The current placeholder may be acceptable for review but should be resolved before publication.

---

## 6. Scope & Referencing — **Rating: 4/5 (Good)**

The topic fits IEEE Transactions on Aerospace and Electronic Systems well: it is about spacecraft swarm coordination architectures, communications sizing, and operational feasibility under constrained links. The paper bridges distributed systems concepts (Raft, SWIM, gossip) with aerospace operational constraints (ISLs, half-duplex RF backup), which is appropriate for TAES.

Referencing is broad and mostly relevant, spanning constellation operations, networking, DTN, AoI, and swarm robotics. The inclusion of CCSDS references (SPP, BPv7, Proximity-1) is appropriate. However, several citations are non-archival (FCC filings, websites, program pages). These are sometimes unavoidable for constellation operations, but the paper should (i) minimize reliance on them for core technical claims, and (ii) add more archival support where possible (e.g., peer-reviewed or standards documents on LEO ISL MACs, phased-array scheduling, or crosslink protocols).

Also, the manuscript positions itself against mega-constellation routing literature, but the connection to *coordination* vs *routing* could be sharpened: readers may ask why DTN/contact scheduling literature does not already solve parts of the “TDMA scheduling and visibility” problem that is currently abstracted into \(\gamma\).

---

## Major Issues

1. **Model boundary confusion: message-layer DES vs TDMA airtime feasibility.**  
   The DES uses a fluid-server ingress and does not enforce half-duplex TDMA slotting (Section III-A, Section IV-D). Yet multiple results and some tables can be read as operational feasibility claims in the RF-backup regime. The manuscript must more explicitly separate: (a) byte-budget feasibility; (b) schedulability under TDMA without retransmissions; (c) schedulability under TDMA with losses/ARQ. A clear “validity domain” label on each major result/table is needed.

2. **Coordinator ingress sizing at 24 kbps is presented too strongly given tight margin and sensitivity.**  
   Table `superframe` leaves 623 ms margin at 24 kbps and \(\gamma=0.85\), shrinking to 98 ms at \(\gamma=0.80\). The paper also shows ARQ infeasibility under correlated loss. The design point is effectively 30 kbps (as the manuscript itself recommends), and the abstract/conclusion should not headline 24 kbps without qualifying it as a minimum no-loss point.

3. **“Topology-invariant command traffic” conclusion depends on a centralized command semantic that should be formalized.**  
   The claim that \(\eta_{\text{cmd}}\) is topology-invariant is only true if every node must receive the same payload volume regardless of architecture. In decentralized or cluster-local planning, command volume/addressing could change substantially (e.g., local consensus, distributed optimization, event-triggered control). The paper should formalize the command model (broadcast vs unicast fraction \(q\), command generation locus) as an explicit assumption and discuss how alternative decision architectures would alter \(\eta_{\text{cmd}}\).

4. **Centralized baseline is compute-only; avoid cross-architecture inference.**  
   Table `topology_comparison` and Fig. `overhead_scaling` include centralized results that are not communications-modeled. While the paper notes this, the presentation still invites comparison. Consider moving centralized compute-queue results to an appendix or clearly separating “compute scalability bound” from “communications overhead.”

5. **Multi-cluster / shared-medium effects are not analyzed but are central to feasibility at scale.**  
   The manuscript acknowledges this as future work, but the main contribution is “sizing for 10³–10⁵ nodes.” At those scales, spectrum reuse, inter-cluster interference, and antenna time-sharing can dominate. Even a simplified analytic reuse model (e.g., frequency reuse factor, number of orthogonal channels, coordinator radio time-sharing across clusters) would materially strengthen the sizing story without requiring full NS-3.

---

## Minor Issues

1. **Equation/notation clarity**
   - Eq. (1) uses \(r\) in \(\lambda = N\cdot r\), but \(r\) is later defined as status reporting rate; ensure consistent naming (status reports vs all message types).
   - Eq. `mesh_messages`: the step from \(O(N f \log N)\) to \(O(N^2)\) depends on choosing \(f=N/\log N\). This is fine but should be stated explicitly in the equation text (currently partially stated).
   - Eq. `unicast_stagger_q`: the \((1+\lfloor qk_c\rfloor)\) term is not fully explained; why “1 + …” rather than \(qk_c\)? Clarify whether it includes the broadcast directive plus unicast subset.

2. **Tables mixing regimes**
   - Table `link_availability` includes \(M_r=2\) results but then warns they apply only to “Regime A.” Consider splitting into two tables or adding a bold header row to prevent misreading.

3. **Overhead accounting vs PHY time**
   - Section IV-A correctly distinguishes “\(\eta\) counts information content” vs airtime. This is crucial; consider moving a short version of this explanation earlier (Section III-F) and referencing it consistently.

4. **Availability numbers appear inconsistent**
   - Table `topology_comparison` lists hierarchical “Graceful (99.5%).” Later, Section IV-I suggests per-coordinator \(A>99.99\%\) and that 99.5% is conservative/cascading. Provide a derivation or reconcile the numbers; otherwise readers may question the robustness claim.

5. **Citation quality**
   - Several key operational claims rely on non-archival sources (Starlink ops, Kuiper overview). Where possible, add archival/technical references (e.g., ITU filings, peer-reviewed constellation ops analyses, or standards).

6. **Figure file naming**
   - `\includegraphics{fig-unicast-stagger}` lacks file extension unlike others; ensure consistency for reproducible builds.

---

## Overall Recommendation — **Major Revision**

The paper has a strong core idea and several valuable analytic results, but it needs substantial revision to (i) tighten the mapping from models to claims, (ii) clarify the validity domains (message-layer vs TDMA airtime vs multi-cluster shared-medium), and (iii) formalize key workload/command assumptions that drive the “topology-invariant” conclusion. With these changes, the manuscript could become a solid TAES contribution; in its current form, readers may over-interpret feasibility conclusions beyond what is validated.

---

## Constructive Suggestions

1. **Add a “Model Validity & Claim Map” table (high impact).**  
   Create a 1-page table that lists each main claim/result (e.g., “\(\eta_0\approx 5\%\)”, “coord ingress 30 kbps”, “ARQ infeasible under per-cycle GE coherence”, “AoI P99=440 s at \(p_{exc}=0.1\)”) and columns: *derived analytically*, *verified by DES*, *verified by slot-level TDMA sim*, *not modeled / future work*. This will immediately resolve boundary confusion.

2. **Promote 30 kbps (or a range) as the practical coordinator PHY sizing result; demote 24 kbps to a minimum bound.**  
   Update abstract, conclusion, and Section IV-A to present: “minimum no-loss schedulable rate ≈24 kbps at \(\gamma=0.85\); recommended design point ≈30 kbps (or \(24–35\) kbps depending on \(\gamma\), ranging, FEC, control).” Consider adding a sensitivity plot of required \(C_{coord}\) vs \(\gamma\) and guard time.

3. **Formalize the workload/command semantic assumptions and provide an alternate scenario.**  
   Define explicitly: who generates commands (ground/regional/cluster), addressing mix \(q\), and whether commands are per-node unique. Then add one alternative scenario (e.g., cluster-local planning reduces command bytes by factor \(\alpha\), but adds intra-cluster consensus overhead) to show how the sizing equations adapt. Even a simple parametric term would make the framework more general.

4. **Introduce a simplified multi-cluster channel reuse/time-sharing model.**  
   Without full NS-3, you can add an analytic constraint such as: number of orthogonal RF channels \(F\), reuse factor \(R\), coordinator radio time-sharing fraction, or maximum simultaneous clusters. This would connect the single-cluster TDMA feasibility to fleet-scale feasibility more credibly.

5. **Rework centralized baseline presentation to avoid misleading comparisons.**  
   Separate “centralized compute queueing bound” from “communications overhead.” Either (i) move centralized compute-only analysis to an appendix, or (ii) add a minimal comms model (even a rough link budget / contact-time constraint) so the baseline is not purely computational.

If you want, I can also provide a marked-up list of specific text edits (abstract/conclusion phrasing, table captions, and where to insert the claim-map table) to align the manuscript with TAES expectations.